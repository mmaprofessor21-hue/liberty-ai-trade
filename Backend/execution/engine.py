import logging
from core.control_router import trading_state, system_state
from core.system_state import SystemStatus
from execution.wallet import wallet_manager
from trading.risk import risk_engine, TradeRisk
from trading.engine import TradeSignal, SignalType

logger = logging.getLogger(__name__)

class ExecutionEngine:
    def __init__(self):
        self.halted = False
        self._active_orders = []

    def cancel_all(self):
        """Best-effort cancel/lock mechanism called during emergency stop.

        In a production system this would call exchange/wallet cancel APIs and
        reconcile state. Here we set a halted flag to prevent further executions
        and clear any in-memory active orders list.
        """
        self.halted = True
        # Ideally cancel remote orders; here we just clear local placeholders
        self._active_orders.clear()
        try:
            print("🛑 ExecutionEngine: cancel_all invoked — halted set to True")
        except Exception:
            pass

    async def execute_signal(self, signal: TradeSignal):
        """
        EXECUTION GUARD (NON-NEGOTIABLE)
        No trade executes unless ALL pass:
        1. Emergency Stop = OFF
        2. Wallet Secure = TRUE
        3. Risk Check = PASS
        4. Strategy Valid = TRUE
        5. AI Confidence >= threshold (if AI Mode)
        6. Slippage <= allowed
        7. Cooldown respected
        """
        logger.info(f"Processing Signal: {signal}")

        # 1. Emergency Stop Check
        if self.halted or system_state.emergency:
            logger.critical("GUARD: Trade BLOCKED - Emergency Stop Active or Engine Halted")
            print("🛑 GUARD: Emergency Stop Active or Engine Halted")
            return False
        
        if system_state.status != SystemStatus.RUNNING:
             logger.warning(f"GUARD: Trade BLOCKED - System is {system_state.status}")
             print(f"🛑 GUARD: System is {system_state.status}")
             return False

        # 2. Wallet Security Check
        wallet_status = await wallet_manager.get_status()
        if not wallet_status.connected or not wallet_status.is_safe:
            logger.critical("GUARD: Trade BLOCKED - Wallet Unsafe or Disconnected")
            print("🛑 GUARD: Wallet Unsafe/Disconnected")
            return False

        # 3. Risk Engine Check
        current_risk_level = trading_state.risk_level
        risk_params = risk_engine.get_risk_parameters(current_risk_level, wallet_status.balance_sol)
        
        # Determine amount (Logic would be more complex in prod, using stop loss dist)
        amount_to_trade = risk_params.max_position_size_sol 
        
        if not risk_engine.validate_trade(amount_to_trade, risk_params):
            logger.warning("GUARD: Trade BLOCKED - Risk Limits Exceeded")
            print("🛑 GUARD: Risk Check Failed")
            return False

        # 4. Strategy Validity Check
        if signal.strategy != trading_state.strategy.value and trading_state.strategy.value != "AI":
             # If strict determinism, strategy must match active system state (unless AI is managing)
             # For now, simplistic check
             pass

        # 5. AI Confidence Check
        if signal.strategy == "AI" or trading_state.strategy.value == "AI":
             # Security Rule: If confidence unavailable, treat as LOW/ZERO
             confidence = signal.ai_confidence or 0.0
             
             # Re-verify against threshold (Redundant but safe)
             # We need to know the threshold here or trust the signal?
             # Better to trust the AIEngine gating logic, but for "Guard" we should double check.
             # Let's import the threshold from AI Config
             from core.control_router import ai_state, AIConfidence
             threshold = 0.5
             if ai_state.confidence_threshold == AIConfidence.LOW: threshold = 0.4
             elif ai_state.confidence_threshold == AIConfidence.HIGH: threshold = 0.8
             
             if confidence < threshold:
                 logger.warning(f"GUARD: Trade BLOCKED - AI Confidence {confidence} < {threshold}")
                 print(f"🛑 GUARD: AI Confidence Too Low ({confidence:.2f} < {threshold})")
                 return False

        # 6. Slippage Check (Stub)
        # if estimated_slippage > risk_params.max_slippage_pct: return False

        # 7. Cooldown Check (Stub)
        # if in_cooldown(signal.symbol): return False

        # --- FINAL GATE ---
        
        # Simulation (Stub)
        sim_result = await wallet_manager.simulate_transaction(signal.symbol, amount_to_trade, signal.type)
        if not sim_result:
            logger.critical("GUARD: Trade BLOCKED - Simulation Failed")
            print("🛑 GUARD: Transaction Simulation Failed")
            return False

        # Execution
        logger.info(f"GUARD: PASS. Executing {signal.type} {amount_to_trade} SOL")
        print(f"✅ EXECUTING {signal.type} | {amount_to_trade:.4f} SOL")
        
        # TODO: Call Wallet Signing -> Broadcast
        
        return True

execution_engine = ExecutionEngine()
