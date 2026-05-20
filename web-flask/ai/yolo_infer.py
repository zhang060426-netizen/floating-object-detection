import hashlib
import importlib.metadata
import importlib.util
import time
from pathlib import Path

from PIL import Image, ImageDraw

CLASS_MAP = {0: "floating_object"}


class InferenceUnavailable(RuntimeError):
    def __init__(self, message, reason="inference_unavailable", details=None):
        super().__init__(message)
        self.reason = reason
        self.details = details or {}


def ultralytics_status():
    spec = importlib.util.find_spec("ultralytics")
    imported = spec is not None
    version = None
    error = None
    if imported:
        try:
            version = importlib.metadata.version("ultralytics")
        except Exception as exc:
            error = str(exc)
    return {
        "ultralytics_import_status": "available" if imported else "missing",
        "ultralytics_importable": imported,
        "ultralytics_version": version,
        "ultralytics_error": error,
    }


def file_sha256(path):
    target = Path(path) if path else None
    if not target or not target.exists() or not target.is_file():
        return None
    digest = hashlib.sha256()
    with target.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_metadata(image_path, filename):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            fmt = img.format.lower() if img.format else Path(filename).suffix.lower().lstrip(".")
    except Exception as exc:
        raise ValueError("invalid image file") from exc
    return {"width": width, "height": height, "filename": filename, "input_format": fmt}


def _load_yolo(weight_path):
    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise InferenceUnavailable(
            "ultralytics dependency is unavailable; real YOLO inference was not executed",
            reason="dependency_unavailable",
            details={"dependency": "ultralytics"},
        ) from exc
    if not Path(weight_path).exists():
        raise InferenceUnavailable(
            f"model weight not found: {weight_path}",
            reason="weight_missing",
            details={"weight_path": str(weight_path)},
        )
    return YOLO(str(weight_path))


def run_yolo_image(image_path, model_row, confidence_threshold=0.5):
    start = time.perf_counter()
    model_load_start = time.perf_counter()
    model = _load_yolo(model_row["weight_path"])
    model_load_ms = (time.perf_counter() - model_load_start) * 1000
    results = model(str(image_path), conf=confidence_threshold, verbose=False)
    inference_ms = (time.perf_counter() - start) * 1000
    postprocess_start = time.perf_counter()
    timings = {"inference_ms": inference_ms, "model_load_ms": model_load_ms}
    if not results:
        timings["postprocess_ms"] = (time.perf_counter() - postprocess_start) * 1000
        return [], timings
    result = results[0]
    detections = []
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        timings["postprocess_ms"] = (time.perf_counter() - postprocess_start) * 1000
        return detections, timings
    xyxy = boxes.xyxy.cpu().tolist() if getattr(boxes, "xyxy", None) is not None else []
    xywhn = boxes.xywhn.cpu().tolist() if getattr(boxes, "xywhn", None) is not None else []
    confs = boxes.conf.cpu().tolist() if getattr(boxes, "conf", None) is not None else []
    clss = boxes.cls.cpu().tolist() if getattr(boxes, "cls", None) is not None else []
    for i, bbox in enumerate(xyxy):
        class_id = int(clss[i]) if i < len(clss) else 0
        if class_id != 0:
            # Preserve current class boundary: only class 0/floating_object is accepted in Phase2B.
            continue
        conf = float(confs[i]) if i < len(confs) else None
        detections.append({
            "detection_id": None,
            "object_index": len(detections),
            "class_id": 0,
            "class_name": CLASS_MAP[0],
            "class_display_name": "漂浮物",
            "confidence": conf,
            "bbox_xyxy": [float(x) for x in bbox],
            "bbox_xywhn": [float(x) for x in xywhn[i]] if i < len(xywhn) else None,
            "bbox_format": "xyxy_pixel",
            "area_px": max(0.0, float(bbox[2] - bbox[0])) * max(0.0, float(bbox[3] - bbox[1])),
            "track_id": None,
            "crop_key": None,
        })
    timings["postprocess_ms"] = (time.perf_counter() - postprocess_start) * 1000
    return detections, timings


def draw_result_image(source_path, target_path, detections):
    with Image.open(source_path).convert("RGB") as img:
        draw = ImageDraw.Draw(img)
        for d in detections:
            x1, y1, x2, y2 = d["bbox_xyxy"]
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            label = f"{d['class_name']} {d['confidence']:.2f}" if d.get("confidence") is not None else d["class_name"]
            draw.text((x1, max(0, y1 - 12)), label, fill="red")
        img.save(target_path)


def build_detection_result(model_row, image_info, detections, artifacts, confidence_threshold, timings=None):
    confidences = [d["confidence"] for d in detections if d.get("confidence") is not None]
    total = len(detections)
    return {
        "schema_version": "detection_result.v1",
        "model": {
            "model_id": model_row["id"],
            "model_name": model_row["name"],
            "base_model": model_row["base_model"],
            "weight_path": model_row["weight_path"],
            "confidence_threshold": confidence_threshold,
            "class_map": {"0": "floating_object"},
        },
        "image": image_info,
        "detections": detections,
        "summary": {
            "total_detections": total,
            "object_count": total,
            "has_detections": total > 0,
            "has_detection": total > 0,
            "detection_status": "detected" if total > 0 else "no_detection",
            "class_counts": {"floating_object": total} if total else {},
            "max_confidence": max(confidences) if confidences else None,
            "avg_confidence": sum(confidences) / len(confidences) if confidences else None,
            "mean_confidence": sum(confidences) / len(confidences) if confidences else None,
        },
        "artifacts": artifacts,
        "timing": timings or {},
    }
