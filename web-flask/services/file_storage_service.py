import datetime as dt
import shutil
import uuid
from pathlib import Path

from flask import current_app
from werkzeug.utils import secure_filename

from config import Config
from utils.paths import ensure_within_root


def validate_bucket(bucket):
    if bucket not in Config.ALLOWED_BUCKETS:
        raise ValueError("invalid bucket")


def make_object_key(prefix, filename):
    safe_name = secure_filename(filename) or "upload.bin"
    suffix = Path(safe_name).suffix.lower()
    stem = Path(safe_name).stem[:40] or "file"
    today = dt.datetime.utcnow()
    return f"{prefix}/{today:%Y/%m/%d}/{uuid.uuid4().hex}_{stem}{suffix}"


def bucket_root(bucket):
    validate_bucket(bucket)
    root = Path(current_app.config["STORAGE_ROOT"]).resolve()
    target = root / bucket
    target.mkdir(parents=True, exist_ok=True)
    return target


def resolve_object_path(bucket, object_key):
    root = bucket_root(bucket)
    return ensure_within_root(root, root / object_key)


def url_for_file(bucket, object_key):
    normalized = object_key.replace(chr(92), "/")
    return f"/api/files/{bucket}/{normalized}"

def file_info(bucket, object_key):
    return {"bucket": bucket, "object_key": object_key, "url": url_for_file(bucket, object_key)}


def save_upload(file_storage, bucket="uploads", prefix="images"):
    filename = file_storage.filename or "upload"
    ext = Path(filename).suffix.lower()
    if ext not in Config.ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("unsupported image type")
    object_key = make_object_key(prefix, filename)
    target = resolve_object_path(bucket, object_key)
    target.parent.mkdir(parents=True, exist_ok=True)
    file_storage.save(target)
    return bucket, object_key, target


def copy_result_image(source_path, original_name):
    ext = Path(original_name).suffix.lower() or ".jpg"
    object_key = make_object_key("images", f"{Path(original_name).stem}_result{ext}")
    target = resolve_object_path("results", object_key)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target)
    return "results", object_key, target

