"""Tests for the DevOps Lab Flask application.
Uses a mock Redis client so tests run without a real Redis server.
"""
import pytest
from unittest.mock import MagicMock, patch
import app as flask_app


@pytest.fixture
def client():
    """Create a test client with a mocked Redis connection."""
    flask_app.app.config["TESTING"] = True
    with patch("app.r", autospec=True) as mock_redis:
        mock_redis.incr.return_value = 42
        mock_redis.get.return_value = "42"
        with flask_app.app.test_client() as c:
            yield c


def test_health(client):
    """Health endpoint always returns status ok."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_index_increments_visits(client):
    """Index route returns a message and visit count."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert "message" in data
    assert "visits" in data
    assert "hostname" in data
    assert data["visits"] == 42


def test_reset_zeros_counter(client):
    """POST /reset sets the counter to zero."""
    res = client.post("/reset")
    assert res.status_code == 200
    data = res.get_json()
    assert data["visits"] == 0
    assert "reset" in data["message"].lower()


def test_reset_requires_post(client):
    """GET /reset must return 405 Method Not Allowed."""
    res = client.get("/reset")
    assert res.status_code == 405


def test_stats_returns_full_info(client):
    """Stats endpoint returns visits, hostname, redis_host."""
    res = client.get("/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert "visits" in data
    assert "hostname" in data
    assert "redis_host" in data
