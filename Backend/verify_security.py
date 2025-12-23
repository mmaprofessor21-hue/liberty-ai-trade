import asyncio
import logging
from core.control_router import trading_state, system_state, RiskLevel, Strategy
from core.system_state import SystemStatus
from execution.engine import execution_engine
from execution.wallet import wallet_manager
from trading.engine import TradeSignal, SignalType

logger = logging.getLogger(__name__)


async def run_security_verification():
    logger.info("--- STARTING SECURITY GUARD VERIFICATION ---")

    # 1. Setup Initial Safe State
    logger.info("\n[Step 1] Setting up Safe State...")
    system_state.status = SystemStatus.RUNNING
    system_state.emergency = False
    trading_state.risk_level = RiskLevel.MEDIUM
    await wallet_manager.connect()

    valid_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0,
        feature_values={}, strategy="STANDARD"
    )

    # 2. Test Emergency Stop (FAIL CLOSED)
    logger.info("\n[Step 2] Testing Emergency Stop (Should BLOCK)...")
    system_state.emergency = True
    res = await execution_engine.execute_signal(valid_signal)
    if not res:
        logger.info("✅ PASS: Emergency Stop blocked trade.")
    else:
        logger.error("❌ FAIL: Emergency Stop ignored!")
    system_state.emergency = False  # Reset

    # 3. Test Paused System (FAIL CLOSED)
    logger.info("\n[Step 3] Testing System Paused (Should BLOCK)...")
    system_state.status = SystemStatus.PAUSED
    res = await execution_engine.execute_signal(valid_signal)
    if not res:
        logger.info("✅ PASS: Paused System blocked trade.")
    else:
        logger.error("❌ FAIL: Paused System ignored!")
    system_state.status = SystemStatus.RUNNING  # Reset

    # 4. Test Wallet Simulation Failure (FAIL CLOSED)
    logger.info("\n[Step 4] Testing Simulation Failure (Should BLOCK)...")
    wallet_manager.status.is_safe = False
    res = await execution_engine.execute_signal(valid_signal)
    if not res:
        logger.info("✅ PASS: Unsafe Wallet blocked trade.")
    else:
        logger.error("❌ FAIL: Unsafe Wallet ignored!")
    wallet_manager.status.is_safe = True

    # 5. Test Happy Path (PASS OPEN)
    logger.info("\n[Step 5] Testing Happy Path (Should PASS)...")
    res = await execution_engine.execute_signal(valid_signal)
    if res:
        logger.info("✅ PASS: Valid trade executed.")
    else:
        logger.error("❌ FAIL: Valid trade blocked unexpectedly!")

    logger.info("\n--- SECURITY VERIFICATION COMPLETE ---")


if __name__ == "__main__":
    asyncio.run(run_security_verification())
