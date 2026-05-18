"""Read-only YOLO runtime adapter for Phase 2B Batch2.

Scope boundaries
----------------
- Does not train or validate models.
- Does not write into weights/, output/, dataset/, or training artifacts.
- Does not modify class definitions: only class_id=0/class_name=floating_object.
- Imports without ultralytics installed; ultralytics is required only for
  ``infer_image`` execution.

The adapter is intentionally small so the Flask backend can consume it during
smoke tests while preserving the frozen ``detection_result.v1`` shape.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

CLASS_ID = 0
CLASS_NAME = "floating_object"
CLASS_MAP = {CLASS_ID: CLASS_NAME}

DEV_MODEL_ID = "m_yolo26n_dev"
DEV_MODEL_NAME = "YOLO26n Dev Baseline"
DEV_BASE_MODEL = "yolo26n"
DEV_WEIGHT_NAME = "yolo26n.pt"
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
DEFAULT_IMGSZ = 640

EXPECTED_DEV_WEIGHT_SIZE_BYTES = 5_544_453
EXPECTED_DEV_WEIGHT_SHA256 = "9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef"


class RuntimeReadinessError(RuntimeError):
    """Raised when runtime prerequisites are unavailable or incompatible."""


def _as_path(path: str | Path) -> Path:
    return path if isinstance(path, Path) else Path(path)


def find_project_root(start: Optional[Path] = None) -> Path:
    """Find the repository/worktree root containing ``other/model_train/detect``."""

    cursor = (start or Path(__file__).resolve()).resolve()
    if cursor.is_file():
        cursor = cursor.parent

    for parent in [cursor, *cursor.parents]:
        if (parent / "other" / "model_train" / "detect").exists():
            return parent
    # Fallback for direct vendoring: yolo_runtime.py -> runtime -> detect -> model_train -> other -> root.
    return Path(__file__).resolve().parents[4]


def resolve_default_weight_path(project_root: Optional[str | Path] = None) -> Path:
    """Return the frozen Phase 2B dev baseline weight path."""

    root = _as_path(project_root).resolve() if project_root else find_project_root()
    return root / "other" / "model_train" / "detect" / "weights" / DEV_WEIGHT_NAME


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute a SHA256 digest without modifying the file."""

    digest = hashlib.sha256()
    with _as_path(path).open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_weight_readiness(
    weight_path: Optional[str | Path] = None,
    *,
    verify_hash: bool = False,
    project_root: Optional[str | Path] = None,
) -> Dict[str, Any]:
    """Return read-only readiness metadata for the dev baseline weight.

    ``verify_hash`` is opt-in because hashing a large file is unnecessary for
    every backend request. Stage smoke checks can enable it explicitly.
    """

    path = _as_path(weight_path).resolve() if weight_path else resolve_default_weight_path(project_root)
    exists = path.exists()
    is_file = path.is_file() if exists else False
    size_bytes = path.stat().st_size if is_file else None
    sha256 = sha256_file(path) if is_file and verify_hash else None

    size_matches = size_bytes == EXPECTED_DEV_WEIGHT_SIZE_BYTES if size_bytes is not None else False
    hash_matches = sha256 == EXPECTED_DEV_WEIGHT_SHA256 if sha256 is not None else None
    ready = bool(is_file and size_matches and (hash_matches is not False))

    return {
        "model_id": DEV_MODEL_ID,
        "weight_name": DEV_WEIGHT_NAME,
        "weight_path": str(path),
        "exists": exists,
        "is_file": is_file,
        "size_bytes": size_bytes,
        "expected_size_bytes": EXPECTED_DEV_WEIGHT_SIZE_BYTES,
        "size_matches": size_matches,
        "sha256": sha256,
        "expected_sha256": EXPECTED_DEV_WEIGHT_SHA256,
        "hash_checked": verify_hash,
        "hash_matches": hash_matches,
        "ready": ready,
        "role": "dev runtime baseline / backend smoke placeholder",
        "production_precision_certified": False,
        "mutation_allowed": False,
    }


def get_dev_model_manifest(
    weight_path: Optional[str | Path] = None,
    *,
    verify_hash: bool = False,
    project_root: Optional[str | Path] = None,
) -> Dict[str, Any]:
    """Return a backend-friendly model manifest for model-list smoke checks."""

    readiness = check_weight_readiness(weight_path, verify_hash=verify_hash, project_root=project_root)
    return {
        "model_id": DEV_MODEL_ID,
        "model_name": DEV_MODEL_NAME,
        "base_model": DEV_BASE_MODEL,
        "weight_name": DEV_WEIGHT_NAME,
        "weight_path": readiness["weight_path"],
        "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD,
        "imgsz": DEFAULT_IMGSZ,
        "class_map": {str(CLASS_ID): CLASS_NAME},
        "is_published": readiness["ready"],
        "stage_role": readiness["role"],
        "limitations": [
            "Development smoke-test baseline only.",
            "No production precision claim.",
            "No training or full dataset validation performed in Batch2 Stage2.",
        ],
        "readiness": readiness,
    }


def _round_float(value: float, digits: int = 6) -> float:
    return round(float(value), digits)


def _coerce_sequence(value: Any) -> List[float]:
    """Convert tensors/arrays/lists from common YOLO result objects to floats."""

    if value is None:
        return []
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "tolist"):
        value = value.tolist()
    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, (list, tuple)) and len(value) == 1 and isinstance(value[0], (list, tuple)):
        value = value[0]
    return [float(item) for item in value]


def _first_result(results: Any) -> Any:
    if isinstance(results, (list, tuple)):
        return results[0] if results else None
    return results


def _image_shape(result: Any, image_path: str | Path) -> Tuple[Optional[int], Optional[int]]:
    orig_shape = getattr(result, "orig_shape", None) if result is not None else None
    if orig_shape and len(orig_shape) >= 2:
        return int(orig_shape[1]), int(orig_shape[0])

    try:
        from PIL import Image  # type: ignore

        with Image.open(image_path) as img:
            return int(img.width), int(img.height)
    except Exception:
        return None, None


def _xywhn_from_xyxy(xyxy: Sequence[float], width: Optional[int], height: Optional[int]) -> List[float]:
    if not width or not height or len(xyxy) != 4:
        return []
    x1, y1, x2, y2 = [float(v) for v in xyxy]
    box_width = max(0.0, x2 - x1)
    box_height = max(0.0, y2 - y1)
    x_center = x1 + box_width / 2
    y_center = y1 + box_height / 2
    return [
        _round_float(x_center / width),
        _round_float(y_center / height),
        _round_float(box_width / width),
        _round_float(box_height / height),
    ]


def _iter_boxes(result: Any) -> Iterable[Any]:
    boxes = getattr(result, "boxes", None) if result is not None else None
    if boxes is None:
        return []
    try:
        return list(boxes)
    except TypeError:
        # Support Ultralytics Boxes container attributes directly.
        xyxy_values = getattr(boxes, "xyxy", [])
        conf_values = getattr(boxes, "conf", [])
        cls_values = getattr(boxes, "cls", [])
        xyxy_rows = xyxy_values.tolist() if hasattr(xyxy_values, "tolist") else xyxy_values
        conf_rows = conf_values.tolist() if hasattr(conf_values, "tolist") else conf_values
        cls_rows = cls_values.tolist() if hasattr(cls_values, "tolist") else cls_values
        return [
            {"xyxy": xyxy, "conf": conf, "cls": cls}
            for xyxy, conf, cls in zip(xyxy_rows, conf_rows, cls_rows)
        ]


def _box_attr(box: Any, name: str) -> Any:
    if isinstance(box, Mapping):
        return box.get(name)
    return getattr(box, name, None)


def normalize_ultralytics_result(
    result: Any,
    *,
    image_path: str | Path,
    model_manifest: Optional[Mapping[str, Any]] = None,
    inference_ms: Optional[float] = None,
) -> Dict[str, Any]:
    """Normalize one Ultralytics result into the frozen Phase 2B shape."""

    first = _first_result(result)
    manifest = dict(model_manifest or get_dev_model_manifest())
    width, height = _image_shape(first, image_path)

    detections: List[Dict[str, Any]] = []
    for index, box in enumerate(_iter_boxes(first)):
        xyxy = _coerce_sequence(_box_attr(box, "xyxy"))
        # Ultralytics single-box tensors may produce [[x1,y1,x2,y2]].
        if len(xyxy) == 1 and isinstance(xyxy[0], list):
            xyxy = [float(v) for v in xyxy[0]]
        conf_seq = _coerce_sequence(_box_attr(box, "conf"))
        cls_seq = _coerce_sequence(_box_attr(box, "cls"))
        class_id = int(cls_seq[0]) if cls_seq else CLASS_ID
        # Phase 2B is single-class only; keep compatible name for unexpected 0-like values.
        class_name = CLASS_MAP.get(class_id, CLASS_NAME if class_id == CLASS_ID else f"unknown_{class_id}")
        confidence = _round_float(conf_seq[0] if conf_seq else 0.0)
        xyxy = [_round_float(v, 3) for v in xyxy[:4]]
        xywhn = _xywhn_from_xyxy(xyxy, width, height)
        area_px = None
        if len(xyxy) == 4:
            area_px = _round_float(max(0.0, xyxy[2] - xyxy[0]) * max(0.0, xyxy[3] - xyxy[1]), 3)

        detections.append(
            {
                "detection_id": f"det_{index}",
                "object_index": index,
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence,
                "bbox": {
                    "format": "xyxy_pixel",
                    "xyxy": xyxy,
                    "xywhn": xywhn,
                },
                # Backward-compatible flat aliases from AI_OUTPUT_SCHEMA.md.
                "bbox_format": "xyxy_pixel",
                "bbox_xyxy": xyxy,
                "bbox_xywhn": xywhn,
                "area_px": area_px,
            }
        )

    confidences = [item["confidence"] for item in detections]
    total = len(detections)
    summary = {
        "total_detections": total,
        "object_count": total,
        "has_detections": total > 0,
        "has_detection": total > 0,
        "max_confidence": max(confidences) if confidences else None,
        "avg_confidence": _round_float(sum(confidences) / total) if confidences else None,
        "mean_confidence": _round_float(sum(confidences) / total) if confidences else None,
        "class_counts": {CLASS_NAME: sum(1 for item in detections if item["class_name"] == CLASS_NAME)},
    }

    return {
        "schema_version": "detection_result.v1",
        "model": {
            "model_id": manifest.get("model_id", DEV_MODEL_ID),
            "model_name": manifest.get("model_name", DEV_MODEL_NAME),
            "base_model": manifest.get("base_model", DEV_BASE_MODEL),
            "weight_name": manifest.get("weight_name", DEV_WEIGHT_NAME),
            "confidence_threshold": manifest.get("confidence_threshold", DEFAULT_CONFIDENCE_THRESHOLD),
        },
        "image": {
            "filename": _as_path(image_path).name,
            "width": width,
            "height": height,
        },
        "detections": detections,
        "summary": summary,
        "timing": {
            "inference_ms": _round_float(inference_ms, 3) if inference_ms is not None else None,
        },
    }


def build_empty_result(
    *,
    image_path: str | Path,
    model_manifest: Optional[Mapping[str, Any]] = None,
    inference_ms: Optional[float] = None,
) -> Dict[str, Any]:
    """Build a successful zero-detection result for tests/fallback plumbing."""

    class EmptyResult:
        boxes: List[Any] = []
        orig_shape: Optional[Tuple[int, int]] = None

    return normalize_ultralytics_result(
        EmptyResult(), image_path=image_path, model_manifest=model_manifest, inference_ms=inference_ms
    )


def infer_image(
    image_path: str | Path,
    *,
    weight_path: Optional[str | Path] = None,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    imgsz: int = DEFAULT_IMGSZ,
    device: Optional[str] = None,
    verify_weight_hash: bool = False,
) -> Dict[str, Any]:
    """Run one read-only YOLO image inference and return detection_result.v1.

    This function intentionally performs no saving. Result image rendering and
    persistence remain backend responsibilities in Phase 2B Batch2.
    """

    image = _as_path(image_path)
    if not image.is_file():
        raise RuntimeReadinessError(f"Image file not found: {image}")

    readiness = check_weight_readiness(weight_path, verify_hash=verify_weight_hash)
    if not readiness["ready"]:
        raise RuntimeReadinessError(
            "Dev baseline weight is not ready: "
            f"path={readiness['weight_path']} exists={readiness['exists']} "
            f"size_matches={readiness['size_matches']} hash_matches={readiness['hash_matches']}"
        )

    try:
        from ultralytics import YOLO  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on optional runtime dependency.
        raise RuntimeReadinessError(
            "ultralytics is required only for real inference; install it in the backend runtime image."
        ) from exc

    started = time.perf_counter()
    model = YOLO(readiness["weight_path"])
    predict_kwargs: Dict[str, Any] = {"conf": confidence_threshold, "imgsz": imgsz, "save": False, "verbose": False}
    if device:
        predict_kwargs["device"] = device
    results = model(str(image), **predict_kwargs)
    inference_ms = (time.perf_counter() - started) * 1000

    manifest = get_dev_model_manifest(readiness["weight_path"], verify_hash=False)
    manifest["confidence_threshold"] = confidence_threshold
    manifest["imgsz"] = imgsz
    return normalize_ultralytics_result(results, image_path=image, model_manifest=manifest, inference_ms=inference_ms)


def _main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 2B Batch2 AI runtime readiness utility")
    parser.add_argument("--check-weight", action="store_true", help="Check dev weight metadata without inference")
    parser.add_argument("--verify-hash", action="store_true", help="Compute SHA256 during weight check")
    parser.add_argument("--weight-path", default=None, help="Override yolo26n.pt path")
    parser.add_argument("--manifest", action="store_true", help="Print dev model manifest")
    args = parser.parse_args(argv)

    payload = (
        get_dev_model_manifest(args.weight_path, verify_hash=args.verify_hash)
        if args.manifest
        else check_weight_readiness(args.weight_path, verify_hash=args.verify_hash)
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.check_weight and not payload.get("ready"):
        return 2
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
