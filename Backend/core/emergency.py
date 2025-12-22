import logging
from core.system_state import SystemStatus
from core.control_router import system_state
from data.engine import data_engine

logger = logging.getLogger(__name__)


def trigger_emergency_stop():
    """
    IMMEDIATE TRADE HALT.
    1. Set the global `system_state` to EMERGENCY.
    2. Ask execution engine to cancel/lock operations.
    3. Broadcast an emergency event to websocket listeners.
    """
    logger.critical("🚨 EMERGENCY STOP TRIGGERED 🚨")
    print("🚨 EMERGENCY STOP TRIGGERED 🚨")

    # 1. Set global state
    system_state.emergency = True
    system_state.status = SystemStatus.EMERGENCY

    # 2. Execution engine cancel/halt (best-effort)
    try:
        from execution.engine import execution_engine
        if hasattr(execution_engine, "cancel_all"):
            execution_engine.cancel_all()
    except Exception:
        # Don't raise in emergency path; log and continue
        logger.exception("Failed to call execution_engine.cancel_all()")

    # 3. Broadcast to websocket listeners so UI updates immediately
    try:
        msg = {"event": "system.health", "payload": {"status": "EMERGENCY"}}
        for q in getattr(data_engine, "listeners", []):
            try:
                q.put_nowait(msg)
            except Exception:
                pass
    except Exception:
        pass

    return True
