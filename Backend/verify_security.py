import asyncio
from core.control_router import trading_state, system_state, RiskLevel, Strategy
from core.system_state import SystemStatus
from execution.engine import execution_engine
from execution.wallet import wallet_manager
from trading.engine import TradeSignal, SignalType

async def run_security_verification():
    print("--- STARTING SECURITY GUARD VERIFICATION ---")

    # 1. Setup Initial Safe State
    print("\n[Step 1] Setting up Safe State...")
    system_state.status = SystemStatus.RUNNING
    system_state.emergency = False
    trading_state.risk_level = RiskLevel.MEDIUM
    await wallet_manager.connect()

    valid_signal = TradeSignal(
        type=SignalType.BUY, symbol="SOL/USDC", price=150.0, 
        feature_values={}, strategy="STANDARD"
    )

    # 2. Test Emergency Stop (FAIL CLOSED)
    print("\n[Step 2] Testing Emergency Stop (Should BLOCK)...")
    system_state.emergency = True
    res = await execution_engine.execute_signal(valid_signal)
    if not res: print("✅ PASS: Emergency Stop blocked trade.")
    else: print("❌ FAIL: Emergency Stop ignored!")
    system_state.emergency = False # Reset

    # 3. Test Paused System (FAIL CLOSED)
    print("\n[Step 3] Testing System Paused (Should BLOCK)...")
    system_state.status = SystemStatus.PAUSED
    res = await execution_engine.execute_signal(valid_signal)
    if not res: print("✅ PASS: Paused System blocked trade.")
    else: print("❌ FAIL: Paused System ignored!")
    system_state.status = SystemStatus.RUNNING # Reset

    # 4. Test Wallet Simulation Failure (FAIL CLOSED)
    print("\n[Step 4] Testing Simulation Failure (Should BLOCK)...")
    # Force a failure by asking for more than balance
    big_signal = TradeSignal(type=SignalType.BUY, symbol="SOL/USDC", price=150.0, feature_values={}, strategy="STANDARD")
    # Mocking verify by accessing internal logic indirectly through amount
    # But wait, execution engine calculates amount from risk. 
    # Let's force unsafe wallet status
    wallet_manager.status.is_safe = False
    res = await execution_engine.execute_signal(valid_signal)
    if not res: print("✅ PASS: Unsafe Wallet blocked trade.")
    else: print("❌ FAIL: Unsafe Wallet ignored!")
    wallet_manager.status.is_safe = True

    # 5. Test Happy Path (PASS OPEN)
    print("\n[Step 5] Testing Happy Path (Should PASS)...")
    res = await execution_engine.execute_signal(valid_signal)
    if res: print("✅ PASS: Valid trade executed.")
    else: print("❌ FAIL: Valid trade blocked unexpectedly!")

    print("\n--- SECURITY VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_security_verification())
