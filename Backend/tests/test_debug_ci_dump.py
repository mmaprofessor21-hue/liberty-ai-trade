import json
import time

def test_write_debug_dump():
    """Writes a small JSON debug dump to Backend/results_debug.txt for CI artifact collection."""
    dump = {"timestamp": time.time()}
    try:
        # execution engine state
        from execution.engine import execution_engine
        dump["execution_halted"] = bool(getattr(execution_engine, "is_halted") and execution_engine.is_halted())
    except Exception as e:
        dump["execution_halted_error"] = str(e)

    try:
        from core.system_state import system_state as core_system_state
        dump["core_system_state"] = {
            "status": getattr(core_system_state, "status", None) and getattr(core_system_state.status, "value", str(core_system_state.status)),
            "emergency": getattr(core_system_state, "emergency", None),
        }
    except Exception as e:
        dump["core_system_state_error"] = str(e)

    try:
        from core.control_router import system_state as api_system_state
        dump["api_system_state"] = {
            "status": getattr(api_system_state, "status", None) and getattr(api_system_state.status, "value", str(api_system_state.status)),
            "emergency": getattr(api_system_state, "emergency", None),
        }
    except Exception as e:
        dump["api_system_state_error"] = str(e)

    try:
        from data.engine import data_engine
        dump["data_engine_listeners"] = len(getattr(data_engine, "listeners", []))
        dump["data_engine_running"] = bool(getattr(data_engine, "running", False))
    except Exception as e:
        dump["data_engine_error"] = str(e)

    with open("Backend/results_debug.txt", "w", encoding="utf-8") as f:
        json.dump(dump, f, indent=2)

    # always pass
    assert True
