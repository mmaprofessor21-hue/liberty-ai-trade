import asyncio
from core.control_router import trading_state, system_state, RiskLevel, Strategy
from core.system_state import SystemStatus
from execution.engine import execution_engine
from execution.wallet import wallet_manager
from trading.engine import TradeSignal, SignalType

async def run_verification():
import logging

logger = logging.getLogger(__name__)

logger.info("--- STARTING PHASE 2 VERIFICATION ---")

    # 1. Setup Initial State
    logger.info("\n[Step 1] Setting up Initial State...")
    system_state.status = SystemStatus.RUNNING
    system_state.emergency = False
    trading_state.risk_level = RiskLevel.MEDIUM
    trading_state.strategy = Strategy.STANDARD
    
    await wallet_manager.connect()
    w_status = await wallet_manager.get_status()
    logger.info(f"Wallet Connected: {w_status.connected}, Balance: {w_status.balance_sol} SOL")

    # 2. Test Valid Trade
    logger.info("\n[Step 2] Testing Valid Trade (Medium Risk)...")
    signal_valid = TradeSignal(
        type=SignalType.BUY,
        symbol="SOL/USDC",
        price=150.0,
        feature_values={},
        strategy="STANDARD_TEST"
    )
    result = await execution_engine.execute_signal(signal_valid)
    logger.info(f"Trade Execution Result: {'SUCCESS' if result else 'FAILED'} (Expected: SUCCESS)")

    # 3. Test High Risk Adjustment
    logger.info("\n[Step 3] Testing High Risk Configuration...")
    trading_state.risk_level = RiskLevel.HIGH
    result = await execution_engine.execute_signal(signal_valid)
    logger.info(f"Trade Execution Result: {'SUCCESS' if result else 'FAILED'} (Expected: SUCCESS with larger size)")

    # 4. Test Emergency Stop
    logger.info("\n[Step 4] Testing Emergency Stop...")
    system_state.emergency = True
    result = await execution_engine.execute_signal(signal_valid)
    logger.info(f"Trade Execution Result: {'SUCCESS' if result else 'FAILED'} (Expected: FAILED)")

    # 5. Reset Emergency
    system_state.emergency = False

    logger.info("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_verification())
