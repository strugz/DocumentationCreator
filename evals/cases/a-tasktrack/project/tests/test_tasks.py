import pytest


def test_title_required(client, logged_in):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Title is required."


@pytest.mark.skip(reason="export not implemented")
def test_export_csv(client, logged_in):
    resp = client.get("/reports/export")
    assert resp.status_code == 200
