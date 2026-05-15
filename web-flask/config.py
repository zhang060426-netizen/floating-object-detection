from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

class Config:
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "phase2b-dev-secret-change-me")
    JWT_SECRET = os.environ.get("JWT_SECRET", SECRET_KEY)
    JWT_EXPIRE_SECONDS = int(os.environ.get("JWT_EXPIRE_SECONDS", "86400"))
    DATABASE = Path(os.environ.get("APP_DB_PATH", BASE_DIR / "storage" / "app.sqlite3")).resolve()
    STORAGE_ROOT = Path(os.environ.get("APP_STORAGE_ROOT", BASE_DIR / "storage")).resolve()
    MAX_CONTENT_LENGTH = int(os.environ.get("APP_UPLOAD_MAX_MB", "16")) * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    ALLOWED_BUCKETS = {"uploads", "results", "models"}
    API_PREFIX = "/api"

    DEFAULT_MODEL_ID = "m_yolo26n_dev"
    DEFAULT_CLASS_MAP = {"0": "floating_object"}
    DEFAULT_CONFIDENCE = 0.5

    @staticmethod
    def model_root() -> Path:
        configured = os.environ.get("AI_MODEL_ROOT")
        if configured:
            return Path(configured).resolve()
        candidates = [
            PROJECT_ROOT / "other" / "model_train" / "detect" / "weights",
            PROJECT_ROOT.parent / "水面漂浮物垃圾检测(YOLO_大模型分析)" / "other" / "model_train" / "detect" / "weights",
            Path("E:/MM/水面漂浮物垃圾检测(YOLO_大模型分析)/other/model_train/detect/weights"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()
        return (BASE_DIR / "storage" / "models").resolve()

    @classmethod
    def default_weight_path(cls) -> Path:
        return cls.model_root() / "yolo26n.pt"
