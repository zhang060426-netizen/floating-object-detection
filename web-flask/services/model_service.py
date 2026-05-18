from pathlib import Path

from ai.yolo_infer import file_sha256, ultralytics_status


def runtime_diagnostic(row):
    weight_path = row["weight_path"] if row else None
    weight_exists = bool(weight_path and Path(weight_path).exists())
    diagnostic = {
        **ultralytics_status(),
        "active_weight_path": weight_path,
        "weight_exists": weight_exists,
        "weight_sha256": file_sha256(weight_path) if weight_exists else None,
        "is_dev_placeholder": bool(row["is_dev_placeholder"]) if row else False,
    }
    return diagnostic


def row_to_model(row):
    if not row:
        return None
    diagnostic = runtime_diagnostic(row)
    return {
        "id": row["id"],
        "name": row["name"],
        "base_model": row["base_model"],
        "weight_path": row["weight_path"],
        "status": "published" if int(row["status"]) == 1 else "draft",
        "is_dev_placeholder": diagnostic["is_dev_placeholder"],
        "weight_exists": diagnostic["weight_exists"],
        "runtime_diagnostic": diagnostic,
    }


def list_published_models(db):
    rows = db.execute("SELECT * FROM models WHERE status = 1 ORDER BY create_time DESC").fetchall()
    return [row_to_model(r) for r in rows]


def get_model(db, model_id):
    return db.execute("SELECT * FROM models WHERE id = ? AND status = 1", (model_id,)).fetchone()
