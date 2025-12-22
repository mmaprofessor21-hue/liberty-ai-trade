import asyncio
from core.control_router import trading_state, system_state, ai_state, RiskLevel, Strategy, AIConfidence
from core.system_state import SystemStatus
from execution.engine import execution_engine
from execution.wallet import wallet_manager
from trading.engine import TradeSignal, SignalType

async def run_ai_verification():
    print("--- STARTING AI INTEGRATION VERIFICATION ---")

    # 1. Setup Safe State
    system_state.status = SystemStatus.RUNNING
    system_state.emergency = False
    trading_state.risk_level = RiskLevel.MEDIUM
    trading_state.strategy = Strategy.AI  # Enable AI Strategy
    await wallet_manager.connect()

    # 2. Test Low Confidence Signal (Should BLOCK)
    print("\n[Step 1] Testing Low Confidence AI Signal (Should BLOCK)...")
    # We manually construct a signal that mimics what TradingEngine would produce
    low_conf_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={}, 
        strategy="AI",
        ai_confidence=0.3, # < Default 0.5 threshold
        ai_explanation="Low confidence test"
    )
    
    # Ensure threshold is standard
    ai_state.confidence_threshold = AIConfidence.MEDIUM # 0.6
    
    res = await execution_engine.execute_signal(low_conf_signal)
    if not res: print(f"✅ PASS: Low confidence signal blocked.")
    else: print(f"❌ FAIL: Low confidence signal executed!")

    # 3. Test High Confidence Signal (Should PASS)
    print("\n[Step 2] Testing High Confidence AI Signal (Should PASS)...")
    high_conf_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={}, 
        strategy="AI",
        ai_confidence=0.9, # > 0.6 threshold
        ai_explanation="High confidence test"
    )
    
    res = await execution_engine.execute_signal(high_conf_signal)
    if res: print(f"✅ PASS: High confidence signal executed.")
    else: print(f"❌ FAIL: High confidence signal blocked!")

    # 4. Test Threshold Adjustment
    print("\n[Step 3] Testing Threshold Adjustment...")
    ai_state.confidence_threshold = AIConfidence.HIGH # 0.8
    medium_conf_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={}, 
        strategy="AI",
        ai_confidence=0.7, # > 0.6 but < 0.8
        ai_explanation="Medium confidence test"
    )
    res = await execution_engine.execute_signal(medium_conf_signal)
    if not res: print(f"✅ PASS: Medium confidence blocked by HIGH threshold.")
    else: print(f"❌ FAIL: Threshold adjustment ignored!")

    print("\n--- AI VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_ai_verification())
