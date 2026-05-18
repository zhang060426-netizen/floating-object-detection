import hashlib
import os
import sqlite3
from pathlib import Path

from flask import current_app, g

from config import Config


def hash_password(password, salt="phase2b"):
    return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()


def verify_password(password, stored):
    # Phase2B accepts the frozen default admin123 and legacy 123456 seeds.
    return hash_password(password) == stored


def get_db():
    if "db" not in g:
        db_path = Path(current_app.config["DATABASE"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def seed_defaults(conn):
    now = "CURRENT_TIMESTAMP"
    users = [
        (1, "admin", hash_password("admin123"), "管理员", 1, 1),
        (2, "test", hash_password("123456"), "测试用户", 0, 1),
    ]
    for row in users:
        conn.execute(
            "INSERT OR IGNORE INTO user(id, username, password, real_name, role, status) VALUES (?, ?, ?, ?, ?, ?)",
            row,
        )
    # Also allow legacy admin/123456 without changing public documented admin/admin123 flow.
    legacy = hash_password("123456")
    admin = conn.execute("SELECT password FROM user WHERE username='admin'").fetchone()
    if admin and admin["password"] not in {hash_password("admin123"), legacy}:
        conn.execute("UPDATE user SET password=? WHERE username='admin'", (hash_password("admin123"),))

    weight_path = str(Config.default_weight_path())
    conn.execute(
        """
        INSERT OR IGNORE INTO models(
            id, name, description, base_model, status, model_bucket, model_object_key,
            weight_path, is_dev_placeholder
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            Config.DEFAULT_MODEL_ID,
            "YOLO26n Dev Baseline",
            "Phase2B development baseline; does not represent historical production accuracy.",
            "yolo26n",
            1,
            "models",
            "yolo26n.pt",
            weight_path,
            1,
        ),
    )
    conn.commit()


def init_db(app=None):
    if app is None:
        app = current_app
    db_path = Path(app.config.get("DATABASE", Config.DATABASE))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    for bucket in Config.ALLOWED_BUCKETS:
        Path(app.config.get("STORAGE_ROOT", Config.STORAGE_ROOT), bucket).mkdir(parents=True, exist_ok=True)
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(schema)
        seed_defaults(conn)
    finally:
        conn.close()
    app.teardown_appcontext(close_db)
