import pytest
from unittest.mock import patch
import app as flask_app


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with patch("app.r") as mock_redis:
        mock_redis.incr.return_value = 42
        mock_redis.get.return_value = "42"
        with flask_app.app.test_client() as client:
            yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_index(client):
    res = client.get("/")
    data = res.get_json()
    assert res.status_code == 200
    assert "message" in data
    assert "visits" in data


def test_reset(client):
    res = client.post("/reset")
    data = res.get_json()
    assert res.status_code == 200
    assert data["visits"] == 0


def test_stats(client):
    res = client.get("/stats")
    data = res.get_json()
    assert res.status_code == 200
    assert "visits" in data
