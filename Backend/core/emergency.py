import logging
from core.system_state import system_state, SystemStatus

logger = logging.getLogger(__name__)

def trigger_emergency_stop():
    """
    Global Emergency Stop Handler (SINGLE SOURCE OF TRUTH)

    Responsibilities:
    1. Set global system_state to EMERGENCY
    2. Halt the execution engine immediately
    3. Be idempotent (safe to call multiple times)
    4. Work in runtime AND tests
    """

    logger.critical("🚨 EMERGENCY STOP TRIGGERED 🚨")

    # Idempotent: if already in emergency, keep going but avoid noisy repeats
    already = bool(getattr(system_state, "emergency", False))
    # 1. Set global system state
    system_state.emergency = True
    system_state.status = SystemStatus.EMERGENCY

    # 2. Halt execution engine (CRITICAL)
    try:
        # IMPORTANT: import the SINGLETON instance
        from execution.engine import execution_engine

        execution_engine.cancel_all()

        logger.critical("🛑 Execution engine halted via emergency stop")

    except Exception as e:
        # Emergency path must NEVER raise
        logger.exception(
            "ExecutionEngine.cancel_all() threw during emergency stop",
            exc_info=e,
        )

    # 3. Broadcast a lightweight emergency event to any connected listeners
    try:
        # lazy import to avoid circulars during test bootstrapping
        from data.engine import data_engine

        msg = {"event": "system.emergency", "payload": {"status": system_state.status.name, "timestamp": __import__('time').time()}}
        for q in getattr(data_engine, "listeners", []):
            try:
                q.put_nowait(msg)
            except Exception:
                # best-effort only
                pass
    except Exception:
        # Do not raise; logging already occurred above for execution_engine
        pass

    # 4. Also attempt to update any module-local system_state copies (best-effort)
    try:
        # control_router historically had its own `system_state` for the API surface.
        from core import control_router
        if hasattr(control_router, "system_state"):
            try:
                control_router.system_state.emergency = True
                control_router.system_state.status = SystemStatus.EMERGENCY
            except Exception:
                pass
    except Exception:
        pass

    # If this was already set previously, return False to indicate no-op; otherwise True
    return not already
