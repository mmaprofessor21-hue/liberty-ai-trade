import pytest

from execution.engine import execution_engine

@pytest.fixture(autouse=True)
def reset_engine():
    """Reset shared execution engine state before each test to avoid cross-test pollution."""
    try:
        if hasattr(execution_engine, "reset_halt"):
            execution_engine.reset_halt()
    except Exception:
        pass
    # Reset global system states used across modules
    try:
        from core.system_state import system_state as core_system_state, SystemStatus
        core_system_state.status = SystemStatus.STOPPED
        core_system_state.emergency = False
    except Exception:
        pass
    try:
        from core.control_router import system_state as api_system_state, SystemConfig
        api_system_state.status = SystemStatus.STOPPED
        api_system_state.emergency = False
    except Exception:
        pass
    yield
