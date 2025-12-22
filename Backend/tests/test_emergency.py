from core.emergency import trigger_emergency_stop
from core.control_router import system_state
from execution.engine import execution_engine


def test_emergency_sets_state_and_halts_engine():
    # Ensure engine is not halted initially
    execution_engine.halted = False
    system_state.emergency = False

    res = trigger_emergency_stop()
    assert res is True
    assert system_state.emergency is True
    assert execution_engine.halted is True
