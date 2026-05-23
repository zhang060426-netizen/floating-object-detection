import json
import sqlite3
from pathlib import Path

import pytest


def _login_headers(client, username="admin", password="admin123"):
    token = __import__("conftest").login(client, username=username, password=password)
    return {"Authorization": f"Bearer {token}"}


def _result(*detections, status=None):
    payload = {
        "schema_version": "detection_result.v1",
        "detections": list(detections),
    }
    if status is not None:
        payload["summary"] = {"detection_status": status, "total_detections": len(detections)}
    return payload


def _insert_record(
    client,
    record_id,
    *,
    user_id=1,
    model_id="m_yolo26n_dev",
    object_key=None,
    detection_result=None,
    raw_detection_result=None,
    create_time="2026-05-22 10:00:00",
):
    db_path = Path(client.application.config["DATABASE"])
    payload = raw_detection_result if raw_detection_result is not None else (
        None if detection_result is None else json.dumps(detection_result, ensure_ascii=False)
    )
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO detection_records(
              id, user_id, model_id, original_image_bucket, original_image_object_key,
              detection_result, confidence_threshold, create_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                user_id,
                model_id,
                "uploads",
                object_key or f"images/{record_id}.png",
                payload,
                0.5,
                create_time,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def _list(client, headers, **query):
    response = client.get("/api/detection/records", headers=headers, query_string=query)
    return response, response.get_json()


def _record_ids(payload):
    return [item["record_id"] for item in payload["data"]["items"]]


def test_records_filters_still_require_jwt(client):
    response = client.get("/api/detection/records", query_string={"keyword": "sample"})

    assert response.status_code == 401


def test_records_unfiltered_response_shape_and_defaults_remain_compatible(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_default", detection_result=_result(status="no_detection"))

    response, payload = _list(client, headers)

    assert response.status_code == 200
    assert set(payload["data"]) == {"items", "total", "page", "page_size"}
    assert payload["data"]["total"] == 1
    assert payload["data"]["page"] == 1
    assert payload["data"]["page_size"] == 20


def test_records_page_page_size_and_page_size_cap_remain_compatible(client):
    headers = _login_headers(client)
    for index in range(3):
        _insert_record(
            client,
            f"dr_page_{index}",
            detection_result=_result(status="no_detection"),
            create_time=f"2026-05-22 10:0{index}:00",
        )

    response, payload = _list(client, headers, page=2, page_size=1)
    capped_response, capped_payload = _list(client, headers, page_size=999)

    assert response.status_code == 200
    assert payload["data"]["total"] == 3
    assert payload["data"]["page"] == 2
    assert payload["data"]["page_size"] == 1
    assert len(payload["data"]["items"]) == 1
    assert capped_response.status_code == 200
    assert capped_payload["data"]["page_size"] == 100


@pytest.mark.parametrize("query", [{"page": "bad"}, {"page_size": "bad"}])
def test_records_reject_non_integer_pagination(client, query):
    response, payload = _list(client, _login_headers(client), **query)

    assert response.status_code == 400
    assert payload["code"] == 400


def test_records_keyword_returns_matching_object_key(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_match", object_key="images/river-waste-sample.png", detection_result=_result(status="detected"))
    _insert_record(client, "dr_other", object_key="images/clear-water.png", detection_result=_result(status="detected"))

    response, payload = _list(client, headers, keyword="WASTE")

    assert response.status_code == 200
    assert payload["data"]["total"] == 1
    assert _record_ids(payload) == ["dr_match"]


def test_records_keyword_no_match_returns_zero_total(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_only", object_key="images/known.png", detection_result=_result(status="detected"))

    response, payload = _list(client, headers, keyword="absent")

    assert response.status_code == 200
    assert payload["data"]["total"] == 0
    assert payload["data"]["items"] == []


def test_records_model_id_filter_is_exact(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_default_model", model_id="m_yolo26n_dev", detection_result=_result(status="detected"))
    _insert_record(client, "dr_other_model", model_id="m_yolo26n_dev_extra", detection_result=_result(status="detected"))

    response, payload = _list(client, headers, model_id="m_yolo26n_dev")

    assert response.status_code == 200
    assert payload["data"]["total"] == 1
    assert _record_ids(payload) == ["dr_default_model"]


def test_records_detection_status_detected(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_detected", detection_result=_result({"confidence": 0.9}, status="detected"))
    _insert_record(client, "dr_empty", detection_result=_result(status="no_detection"))

    response, payload = _list(client, headers, detection_status="detected")

    assert response.status_code == 200
    assert _record_ids(payload) == ["dr_detected"]


def test_records_detection_status_no_detection(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_detected", detection_result=_result({"confidence": 0.9}, status="detected"))
    _insert_record(client, "dr_empty", detection_result=_result(status="no_detection"))

    response, payload = _list(client, headers, detection_status="no_detection")

    assert response.status_code == 200
    assert _record_ids(payload) == ["dr_empty"]


def test_records_detection_status_unknown_includes_missing_result(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_missing", detection_result=None)

    response, payload = _list(client, headers, detection_status="unknown")

    assert response.status_code == 200
    assert _record_ids(payload) == ["dr_missing"]


def test_records_detection_status_unknown_includes_malformed_result(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_malformed", raw_detection_result="{not-json")

    response, payload = _list(client, headers, detection_status="unknown")

    assert response.status_code == 200
    assert _record_ids(payload) == ["dr_malformed"]


def test_records_detection_status_supports_legacy_and_old_records(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_success", detection_result=_result(status="success"))
    _insert_record(client, "dr_empty", detection_result=_result(status="empty"))
    _insert_record(client, "dr_old_detected", detection_result=_result({"confidence": 0.7}))

    detected_response, detected_payload = _list(client, headers, detection_status="detected")
    empty_response, empty_payload = _list(client, headers, detection_status="no_detection")

    assert detected_response.status_code == 200
    assert set(_record_ids(detected_payload)) == {"dr_success", "dr_old_detected"}
    assert empty_response.status_code == 200
    assert _record_ids(empty_payload) == ["dr_empty"]


@pytest.mark.parametrize("status", ["pending", "DETECTED"])
def test_records_reject_invalid_detection_status(client, status):
    response, payload = _list(client, _login_headers(client), detection_status=status)

    assert response.status_code == 400
    assert payload["code"] == 400


def test_records_date_range_filters_create_time_inclusively(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_before", detection_result=_result(status="detected"), create_time="2026-05-01 23:59:59")
    _insert_record(client, "dr_start", detection_result=_result(status="detected"), create_time="2026-05-02 00:00:00")
    _insert_record(client, "dr_end", detection_result=_result(status="detected"), create_time="2026-05-03 23:59:59")
    _insert_record(client, "dr_after", detection_result=_result(status="detected"), create_time="2026-05-04 00:00:00")

    response, payload = _list(client, headers, date_start="2026-05-02", date_end="2026-05-03")

    assert response.status_code == 200
    assert payload["data"]["total"] == 2
    assert set(_record_ids(payload)) == {"dr_start", "dr_end"}


def test_records_reject_inverted_date_range(client):
    response, payload = _list(client, _login_headers(client), date_start="2026-05-04", date_end="2026-05-03")

    assert response.status_code == 400
    assert payload["code"] == 400


@pytest.mark.parametrize("query", [{"date_start": "2026-13-01"}, {"date_end": "not-a-date"}])
def test_records_reject_invalid_date_formats(client, query):
    response, payload = _list(client, _login_headers(client), **query)

    assert response.status_code == 400
    assert payload["code"] == 400


def test_records_normal_user_filters_stay_within_owned_records(client):
    headers = _login_headers(client, username="test", password="123456")
    _insert_record(client, "dr_owned", user_id=2, object_key="images/shared-match-owned.png", detection_result=_result(status="detected"))
    _insert_record(client, "dr_admin", user_id=1, object_key="images/shared-match-admin.png", detection_result=_result(status="detected"))

    response, payload = _list(client, headers, keyword="shared-match", detection_status="detected")

    assert response.status_code == 200
    assert payload["data"]["total"] == 1
    assert _record_ids(payload) == ["dr_owned"]


def test_records_admin_filters_can_see_global_records(client):
    headers = _login_headers(client)
    _insert_record(client, "dr_owned", user_id=2, object_key="images/global-match-owned.png", detection_result=_result(status="detected"))
    _insert_record(client, "dr_admin", user_id=1, object_key="images/global-match-admin.png", detection_result=_result(status="detected"))

    response, payload = _list(client, headers, keyword="global-match", detection_status="detected")

    assert response.status_code == 200
    assert payload["data"]["total"] == 2
    assert set(_record_ids(payload)) == {"dr_owned", "dr_admin"}


def test_records_filters_are_applied_before_pagination_and_total(client):
    headers = _login_headers(client)
    for index in range(3):
        _insert_record(
            client,
            f"dr_detected_{index}",
            object_key=f"images/paged-{index}.png",
            detection_result=_result({"confidence": 0.8}, status="detected"),
            create_time=f"2026-05-22 10:0{index}:00",
        )
    _insert_record(
        client,
        "dr_not_detected",
        object_key="images/paged-empty.png",
        detection_result=_result(status="no_detection"),
        create_time="2026-05-22 10:03:00",
    )

    response, payload = _list(client, headers, keyword="paged", detection_status="detected", page=2, page_size=1)

    assert response.status_code == 200
    assert payload["data"]["total"] == 3
    assert payload["data"]["page"] == 2
    assert payload["data"]["page_size"] == 1
    assert len(payload["data"]["items"]) == 1
