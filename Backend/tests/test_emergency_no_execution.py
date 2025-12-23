import asyncio
from core.emergency import trigger_emergency_stop
from core.system_state import SystemStatus, system_state
from execution.engine import execution_engine
from trading.engine import TradeSignal, SignalType


def test_no_execution_after_emergency():
    # Prepare clean state
    system_state.status = SystemStatus.RUNNING
    system_state.emergency = False
    if hasattr(execution_engine, "reset_halt"):
        execution_engine.reset_halt()

    # Trigger emergency
    changed = trigger_emergency_stop()
    assert system_state.emergency is True
    assert system_state.status == SystemStatus.EMERGENCY
    assert execution_engine.is_halted() is True

    # Build a dummy signal
    sig = TradeSignal(type=SignalType.BUY, symbol="SOL/USDC", price=100.0, feature_values={}, strategy="STANDARD")

    # Ensure execute_signal returns False under emergency
    result = asyncio.run(execution_engine.execute_signal(sig))
    assert result is False
