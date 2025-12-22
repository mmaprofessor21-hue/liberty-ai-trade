from core.telegram_interface import telegram_bot
from core.system_state import SystemStatus
from core.control_router import trading_state, Strategy, system_state

async def run_telegram_verification():
    print("--- STARTING AUTOMATION & TELEGRAM VERIFICATION ---")
    
    user_id = 123456789 # Whitelisted ID
    
    # 1. Test Status
    print("\n[Step 1] Testing /STATUS...")
    res = await telegram_bot.handle_command(user_id, "/STATUS", [])
    print(f"Response: {res}")
    
    # 2. Test Strategy Change
    print("\n[Step 2] Testing /STRATEGY SCALP...")
    res = await telegram_bot.handle_command(user_id, "/STRATEGY", ["SCALP"])
    if trading_state.strategy == Strategy.SCALP:
        print("✅ PASS: Strategy changed to SCALP via Telegram.")
    else:
        print("❌ FAIL: Strategy change failed.")
        
    # 3. Test Emergency Stop (Remote)
    print("\n[Step 3] Testing /EMERGENCY...")
    res = await telegram_bot.handle_command(user_id, "/EMERGENCY", [])
    if system_state.emergency and system_state.status == SystemStatus.STOPPED:
        print("✅ PASS: Emergency Stop triggered via Telegram.")
    else:
         print("❌ FAIL: Emergency Stop failed.")

    # 4. Test Override Attempt (Failure Expected)
    print("\n[Step 4] Testing Remote Override of Emergency Stop (/START)...")
    res = await telegram_bot.handle_command(user_id, "/START", [])
    if "Cannot execute commands" in res and system_state.emergency:
        print("✅ PASS: Remote START blocked by Emergency State.")
    else:
        print(f"❌ FAIL: Block failed! Res: {res}")

    print("\n--- AUTOMATION VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(run_telegram_verification())
