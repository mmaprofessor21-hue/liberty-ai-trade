import os
from fastapi.testclient import TestClient

from main import app

from core.control_router import system_state
from core.system_state import SystemStatus

from execution.engine import execution_engine


def test_emergency_via_api_sets_halt(monkeypatch):
    # Arrange: ensure ADMIN_API_KEY is set for the require_admin dependency
    monkeypatch.setenv("ADMIN_API_KEY", "test_admin_key")

    client = TestClient(app)

    # Sanity pre-check
    assert not execution_engine.is_halted()
    assert system_state.status != SystemStatus.EMERGENCY

    # Act: call the control endpoint to trigger emergency
    resp = client.post(
        "/api/v1/controls/system",
        headers={"X-API-KEY": "test_admin_key"},
        json={"emergency": True, "status": SystemStatus.EMERGENCY.value},
    )

    # Assert: API indicates updated system and execution engine halted
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body.get("status") == "updated"

    # Execution engine should be halted and system_state set to EMERGENCY
    assert execution_engine.is_halted() is True
    assert system_state.emergency is True
    assert system_state.status == SystemStatus.EMERGENCY

    # Cleanup: reset for other tests
    system_state.emergency = False
    system_state.status = SystemStatus.STOPPED
    # Note: execution_engine.cancel_all() sets halted; there's no cancel reset here.
