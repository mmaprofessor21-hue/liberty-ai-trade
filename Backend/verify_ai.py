import asyncio
import logging

from core.control_router import trading_state, system_state, ai_state, RiskLevel, Strategy, AIConfidence
from core.system_state import SystemStatus
from execution.engine import execution_engine
from execution.wallet import wallet_manager
from trading.engine import TradeSignal, SignalType

logger = logging.getLogger(__name__)


async def run_ai_verification():
    logger.info("--- STARTING AI INTEGRATION VERIFICATION ---")

    # 1. Setup Safe State
    system_state.status = SystemStatus.RUNNING
    system_state.emergency = False
    trading_state.risk_level = RiskLevel.MEDIUM
    trading_state.strategy = Strategy.AI  # Enable AI Strategy
    await wallet_manager.connect()

    # 2. Test Low Confidence Signal (Should BLOCK)
    logger.info("\n[Step 1] Testing Low Confidence AI Signal (Should BLOCK)...")
    low_conf_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={},
        strategy="AI",
        ai_confidence=0.3,
        ai_explanation="Low confidence test",
    )

    ai_state.confidence_threshold = AIConfidence.MEDIUM
    res = await execution_engine.execute_signal(low_conf_signal)
    if not res:
        logger.info("✅ PASS: Low confidence signal blocked.")
    else:
        logger.error("❌ FAIL: Low confidence signal executed!")

    # 3. Test High Confidence Signal (Should PASS)
    logger.info("\n[Step 2] Testing High Confidence AI Signal (Should PASS)...")
    high_conf_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={},
        strategy="AI",
        ai_confidence=0.9,
        ai_explanation="High confidence test",
    )

    res = await execution_engine.execute_signal(high_conf_signal)
    if res:
        logger.info("✅ PASS: High confidence signal executed.")
    else:
        logger.error("❌ FAIL: High confidence signal blocked!")

    # 4. Test Threshold Adjustment
    logger.info("\n[Step 3] Testing Threshold Adjustment...")
    ai_state.confidence_threshold = AIConfidence.HIGH
    medium_conf_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={},
        strategy="AI",
        ai_confidence=0.7,
        ai_explanation="Medium confidence test",
    )
    res = await execution_engine.execute_signal(medium_conf_signal)
    if not res:
        logger.info("✅ PASS: Medium confidence blocked by HIGH threshold.")
    else:
        logger.error("❌ FAIL: Threshold adjustment ignored!")

    logger.info("\n--- AI VERIFICATION COMPLETE ---")


if __name__ == "__main__":
    asyncio.run(run_ai_verification())
