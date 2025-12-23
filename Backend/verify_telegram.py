import asyncio
import logging
from core.telegram_interface import telegram_bot
from core.system_state import SystemStatus
from core.control_router import trading_state, Strategy, system_state

logger = logging.getLogger(__name__)


async def run_telegram_verification():
    logger.info("--- STARTING AUTOMATION & TELEGRAM VERIFICATION ---")

    user_id = 123456789  # Whitelisted ID

    # 1. Test Status
    logger.info("\n[Step 1] Testing /STATUS...")
    res = await telegram_bot.handle_command(user_id, "/STATUS", [])
    logger.info(f"Response: {res}")

    # 2. Test Strategy Change
    logger.info("\n[Step 2] Testing /STRATEGY SCALP...")
    res = await telegram_bot.handle_command(user_id, "/STRATEGY", ["SCALP"])
    if trading_state.strategy == Strategy.SCALP:
        logger.info("✅ PASS: Strategy changed to SCALP via Telegram.")
    else:
        logger.error("❌ FAIL: Strategy change failed.")

    # 3. Test Emergency Stop (Remote)
    logger.info("\n[Step 3] Testing /EMERGENCY...")
    res = await telegram_bot.handle_command(user_id, "/EMERGENCY", [])
    if system_state.emergency and system_state.status == SystemStatus.STOPPED:
        logger.info("✅ PASS: Emergency Stop triggered via Telegram.")
    else:
        logger.error("❌ FAIL: Emergency Stop failed.")

    # 4. Test Override Attempt (Failure Expected)
    logger.info("\n[Step 4] Testing Remote Override of Emergency Stop (/START)...")
    res = await telegram_bot.handle_command(user_id, "/START", [])
    if "Cannot execute commands" in res and system_state.emergency:
        logger.info("✅ PASS: Remote START blocked by Emergency State.")
    else:
        logger.error(f"❌ FAIL: Block failed! Res: {res}")

    logger.info("\n--- AUTOMATION VERIFICATION COMPLETE ---")


if __name__ == "__main__":
    asyncio.run(run_telegram_verification())
