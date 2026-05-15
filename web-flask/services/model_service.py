from pathlib import Path

from config import Config


def row_to_model(row):
    if not row:
        return None
    return {
        "id": row["id"],
        "name": row["name"],
        "base_model": row["base_model"],
        "weight_path": row["weight_path"],
        "status": "published" if int(row["status"]) == 1 else "draft",
        "is_dev_placeholder": bool(row["is_dev_placeholder"]),
        "weight_exists": bool(row["weight_path"] and Path(row["weight_path"]).exists()),
    }


def list_published_models(db):
    rows = db.execute("SELECT * FROM models WHERE status = 1 ORDER BY create_time DESC").fetchall()
    return [row_to_model(r) for r in rows]


def get_model(db, model_id):
    return db.execute("SELECT * FROM models WHERE id = ? AND status = 1", (model_id,)).fetchone()
