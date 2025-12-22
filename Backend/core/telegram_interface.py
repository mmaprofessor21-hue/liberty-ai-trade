from core.system_state import SystemStatus
from core.control_router import trading_state, Strategy, system_state
from utils.logger import system_logger

# Mocking Telegram Context for structure
class TelegramInterface:
    def __init__(self, token=None):
        self.token = token
        # In real impl, we'd start the Updater here
    
    async def handle_command(self, user_id: int, command: str, args: list):
        """
        Processes commands from Telegram.
        ENFORCES SECURITY SCOPE.
        """
        system_logger.log_event("TELEGRAM_CMD", {"user_id": user_id, "command": command})
        
        # 0. Auth Check (Stub)
        if user_id not in [123456789]: # Whitelist
             return "⛔ Unauthorized access."

        command = command.upper()

        # 1. STOP (Always Allowed)
        if command == "/STOP":
            system_state.status = SystemStatus.STOPPED
            return "🛑 System STOPPED by Remote Command."

        # 2. EMERGENCY STOP (Always Allowed)
        if command == "/EMERGENCY":
            system_state.emergency = True
            system_state.status = SystemStatus.STOPPED
            return "🚨 EMERGENCY STOP TRIGGERED REMOTE 🚨"

        # 3. Security Check: Cannot override Emergency
        if system_state.emergency:
            return "❌ Cannot execute commands. EMERGENCY STATE ACTIVE. Manual reset required."

        # 4. START
        if command == "/START":
            system_state.status = SystemStatus.RUNNING
            return "✅ System STARTED."

        # 5. STATUS
        if command == "/STATUS":
            return f"Status: {system_state.status}\nStrategy: {trading_state.strategy}\nEmerg: {system_state.emergency}"

        # 6. STRATEGY
        if command == "/STRATEGY":
            if not args: return "Usage: /strategy [STANDARD|SCALP|AI]"
            strat = args[0].upper()
            try:
                trading_state.strategy = Strategy(strat)
                return f"✅ Strategy switched to {strat}"
            except ValueError:
                return f"❌ Invalid strategy: {strat}"

        return "❓ Unknown command."

telegram_bot = TelegramInterface()
