import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE": str(tmp_path / "app.sqlite3"),
        "STORAGE_ROOT": str(tmp_path / "storage"),
        "JWT_SECRET": "test-secret",
    })
    return app.test_client()


def login(client, username="admin", password="admin123"):
    rv = client.post("/api/auth/login", json={"username": username, "password": password})
    assert rv.status_code == 200, rv.get_json()
    return rv.get_json()["data"]["token"]
