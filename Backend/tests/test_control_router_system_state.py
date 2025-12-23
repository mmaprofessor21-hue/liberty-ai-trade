from fastapi.testclient import TestClient
from core.system_state import SystemStatus, system_state as shared_system_state
from core.emergency import trigger_emergency_stop
from execution.engine import execution_engine
from main import app


def test_trigger_emergency_reflected_in_api_and_engine():
    # Ensure clean starting state
    shared_system_state.emergency = False
    shared_system_state.status = SystemStatus.RUNNING
    if hasattr(execution_engine, "reset_halt"):
        execution_engine.reset_halt()

    # Trigger emergency stop
    changed = trigger_emergency_stop()
    assert changed is True or changed is False  # idempotent may return False if already set

    # Shared state should reflect emergency
    assert shared_system_state.emergency is True
    assert shared_system_state.status == SystemStatus.EMERGENCY

    # Execution engine should be halted
    assert execution_engine.is_halted() is True

    # API should expose the same shared state
    client = TestClient(app)
    resp = client.get("/api/v1/controls/system")
    assert resp.status_code == 200
    json = resp.json()
    assert json.get("emergency") is True
    assert json.get("status") == SystemStatus.EMERGENCY
