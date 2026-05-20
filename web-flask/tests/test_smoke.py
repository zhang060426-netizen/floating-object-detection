from services.model_service import list_published_models
from db.init_db import get_db


def test_health(client):
    rv = client.get("/api/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["code"] == 0
    assert data["data"]["status"] == "ok"


def test_login_success_and_failure(client):
    ok = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert ok.status_code == 200
    assert ok.get_json()["data"]["token"]
    bad = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert bad.status_code == 401


def test_unauthorized_business_api(client):
    rv = client.get("/api/models/published")
    assert rv.status_code == 401
    assert rv.get_json()["code"] == 401


def test_db_init_models_and_records_schema(client):
    token = __import__("conftest").login(client)
    rv = client.get("/api/models/published", headers={"Authorization": f"Bearer {token}"})
    assert rv.status_code == 200
    models = rv.get_json()["data"]
    assert models and models[0]["id"] == "m_yolo26n_dev"

    record = client.post(
        "/api/detection/records",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model_id": "m_yolo26n_dev",
            "original_image": {"bucket": "uploads", "object_key": "images/test.png"},
            "result_image": {"bucket": "results", "object_key": "images/test_result.png"},
            "detection_result": {
                "schema_version": "detection_result.v1",
                "detections": [],
                "summary": {"total_detections": 0, "has_detections": False},
            },
        },
    )
    assert record.status_code == 200, record.get_json()
    record_id = record.get_json()["data"]["record_id"]

    listing = client.get("/api/detection/records", headers={"Authorization": f"Bearer {token}"})
    assert listing.status_code == 200
    assert listing.get_json()["data"]["total"] == 1

    detail = client.get(f"/api/detection/records/{record_id}", headers={"Authorization": f"Bearer {token}"})
    assert detail.status_code == 200
    payload = detail.get_json()["data"]
    assert payload["detection_result"]["schema_version"] == "detection_result.v1"
    assert "timing" not in payload["detection_result"]
    assert payload["original_image"]["url"].startswith("/api/files/uploads/")
