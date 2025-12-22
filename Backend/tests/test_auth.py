import os
import jwt
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_api_key_allows_control_post(monkeypatch):
    # Ensure ADMIN_API_KEY is set
    monkeypatch.setenv("ADMIN_API_KEY", "test-admin-key")

    payload = {
        "logging_mode": "NORMAL",
        "risk_level": "MEDIUM",
        "sniping_mode": False,
        "strategy": "STANDARD",
    }

    resp = client.post("/api/v1/controls/trading", json=payload, headers={"X-API-KEY": "test-admin-key"})
    assert resp.status_code == 200
    assert resp.json().get("status") == "updated"


def test_jwt_admin_allows_control_post(monkeypatch):
    # Remove ADMIN_API_KEY to force JWT path
    monkeypatch.delenv("ADMIN_API_KEY", raising=False)
    monkeypatch.setenv("JWT_SECRET_KEY", "jwt-secret-test-0123456789")

    token = jwt.encode({"roles": ["admin"]}, os.environ["JWT_SECRET_KEY"], algorithm="HS256")

    payload = {
        "logging_mode": "NORMAL",
        "risk_level": "MEDIUM",
        "sniping_mode": False,
        "strategy": "STANDARD",
    }

    resp = client.post(
        "/api/v1/controls/trading",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json().get("status") == "updated"
