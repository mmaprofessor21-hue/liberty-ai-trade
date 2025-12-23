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
    print("🚨 EMERGENCY STOP TRIGGERED 🚨")

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

    # 3. Broadcast / telemetry hooks can live here later
    return True
