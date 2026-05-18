"""Phase 2B Batch2 AI runtime readiness package.

This package exposes a small, backend-consumable YOLO runtime adapter without
training, validating, mutating model weights, or changing class definitions.
"""

from .yolo_runtime import (
    CLASS_ID,
    CLASS_NAME,
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_IMGSZ,
    DEV_MODEL_ID,
    DEV_MODEL_NAME,
    DEV_WEIGHT_NAME,
    EXPECTED_DEV_WEIGHT_SHA256,
    EXPECTED_DEV_WEIGHT_SIZE_BYTES,
    RuntimeReadinessError,
    build_empty_result,
    check_weight_readiness,
    get_dev_model_manifest,
    infer_image,
    normalize_ultralytics_result,
    resolve_default_weight_path,
)

__all__ = [
    "CLASS_ID",
    "CLASS_NAME",
    "DEFAULT_CONFIDENCE_THRESHOLD",
    "DEFAULT_IMGSZ",
    "DEV_MODEL_ID",
    "DEV_MODEL_NAME",
    "DEV_WEIGHT_NAME",
    "EXPECTED_DEV_WEIGHT_SHA256",
    "EXPECTED_DEV_WEIGHT_SIZE_BYTES",
    "RuntimeReadinessError",
    "build_empty_result",
    "check_weight_readiness",
    "get_dev_model_manifest",
    "infer_image",
    "normalize_ultralytics_result",
    "resolve_default_weight_path",
]
