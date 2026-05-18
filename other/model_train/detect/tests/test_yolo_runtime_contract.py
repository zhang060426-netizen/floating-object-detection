import tempfile
import unittest
from pathlib import Path

from other.model_train.detect.runtime import yolo_runtime as rt


class FakeBox:
    def __init__(self, xyxy, conf, cls):
        self.xyxy = xyxy
        self.conf = conf
        self.cls = cls


class FakeResult:
    orig_shape = (720, 1280)

    def __init__(self, boxes):
        self.boxes = boxes


class RuntimeContractTests(unittest.TestCase):
    def test_normalize_single_detection_contract(self):
        result = FakeResult([FakeBox([100, 120, 240, 260], [0.86], [0])])

        payload = rt.normalize_ultralytics_result(result, image_path="sample.jpg", inference_ms=12.3456)

        self.assertEqual(payload["schema_version"], "detection_result.v1")
        self.assertEqual(payload["model"]["model_id"], "m_yolo26n_dev")
        self.assertEqual(payload["image"]["width"], 1280)
        self.assertEqual(payload["image"]["height"], 720)
        self.assertEqual(payload["summary"]["total_detections"], 1)
        self.assertTrue(payload["summary"]["has_detections"])
        det = payload["detections"][0]
        self.assertEqual(det["class_id"], 0)
        self.assertEqual(det["class_name"], "floating_object")
        self.assertEqual(det["bbox"]["format"], "xyxy_pixel")
        self.assertEqual(det["bbox"]["xyxy"], [100.0, 120.0, 240.0, 260.0])
        self.assertEqual(det["bbox"]["xywhn"], [0.132812, 0.263889, 0.109375, 0.194444])

    def test_empty_result_is_successful_contract(self):
        payload = rt.build_empty_result(image_path="empty.jpg")

        self.assertEqual(payload["detections"], [])
        self.assertEqual(payload["summary"]["total_detections"], 0)
        self.assertFalse(payload["summary"]["has_detections"])
        self.assertEqual(payload["summary"]["class_counts"], {"floating_object": 0})

    def test_missing_weight_readiness_is_non_mutating_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "yolo26n.pt"
            readiness = rt.check_weight_readiness(missing, verify_hash=True)

        self.assertFalse(readiness["ready"])
        self.assertFalse(readiness["exists"])
        self.assertFalse(readiness["mutation_allowed"])
        self.assertFalse(readiness["production_precision_certified"])
        self.assertEqual(readiness["expected_sha256"], rt.EXPECTED_DEV_WEIGHT_SHA256)


if __name__ == "__main__":
    unittest.main()
