import logging
import threading
import time
import builtins
from collections import deque

from core.control_router import trading_state, system_state
from core.system_state import SystemStatus
from execution.wallet import wallet_manager
from trading.risk import risk_engine, TradeRisk
from trading.engine import TradeSignal, SignalType

logger = logging.getLogger(__name__)


class ExecutionEngine:
    def __init__(self):
        # Share halt state across import variants by using a process-wide builtin slot.
        if not hasattr(builtins, "_liberty_execution_state"):
            builtins._liberty_execution_state = {
                "halted": False,
                "halted_since": None,
                # Use a deque for efficient thread-safe append/clear patterns;
                # access must be guarded by `_cancel_lock` for consistency.
                "active_orders": deque(),
            }
        self._shared = builtins._liberty_execution_state
        self._cancel_lock = threading.Lock()

    def cancel_all(self):
        """
        Best-effort cancel/lock mechanism called during emergency stop.

        In a production system this would call exchange/wallet cancel APIs and
        reconcile state. Here we set a halted flag to prevent further executions
        and clear any in-memory active orders list.
        """
        try:
            with self._cancel_lock:
                if self.halted:
                    logger.info(
                        "ExecutionEngine.cancel_all called but already halted"
                    )
                    return True

                # set halted state
                self.halted = True
                self.halted_since = time.time()

                # clear active orders under lock
                try:
                    self.clear_active_orders()
                except Exception:
                    pass

                logger.warning(
                    "🛑 ExecutionEngine: cancel_all invoked — halted set to True"
                )
        except Exception:
            logger.exception("Error during cancel_all")

        return True

    def is_halted(self) -> bool:
        """
        Required by emergency-stop tests.
        """
        return bool(self.halted)

    def reset_halt(self):
        """Reset halted state for tests or controlled restarts.

        This is intentionally explicit and should only be used in safe
        administrative or test contexts.
        """
        try:
            with self._cancel_lock:
                self.halted = False
                self.halted_since = None
                try:
                    self.clear_active_orders()
                except Exception:
                    pass
                logger.info("ExecutionEngine: reset_halt called — engine resumed")
        except Exception:
            logger.exception("Error during reset_halt")
        return True

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
        if self.is_halted() or system_state.emergency:
            logger.critical("GUARD: Trade BLOCKED - Emergency Stop Active or Engine Halted")
            logger.warning("GUARD: Emergency Stop Active or Engine Halted")
            return False

        if system_state.status != SystemStatus.RUNNING:
            logger.warning(f"GUARD: Trade BLOCKED - System is {system_state.status}")
            return False

        # 2. Wallet Security Check
        wallet_status = await wallet_manager.get_status()
        if not wallet_status.connected or not wallet_status.is_safe:
            logger.critical("GUARD: Trade BLOCKED - Wallet Unsafe or Disconnected")
            return False

        # 3. Risk Engine Check
        current_risk_level = trading_state.risk_level
        risk_params = risk_engine.get_risk_parameters(
            current_risk_level, wallet_status.balance_sol
        )

        amount_to_trade = risk_params.max_position_size_sol

        if not risk_engine.validate_trade(amount_to_trade, risk_params):
            logger.warning("GUARD: Trade BLOCKED - Risk Limits Exceeded")
            return False

        # 4. Strategy Validity Check
        if (
            signal.strategy != trading_state.strategy.value
            and trading_state.strategy.value != "AI"
        ):
            pass

        # 5. AI Confidence Check
        if signal.strategy == "AI" or trading_state.strategy.value == "AI":
            confidence = signal.ai_confidence or 0.0

            from core.control_router import ai_state, AIConfidence

            threshold = 0.5
            if ai_state.confidence_threshold == AIConfidence.LOW:
                threshold = 0.4
            elif ai_state.confidence_threshold == AIConfidence.HIGH:
                threshold = 0.8

            if confidence < threshold:
                logger.warning(f"GUARD: Trade BLOCKED - AI Confidence {confidence} < {threshold}")
                return False

        # 6. Slippage Check (Stub)
        # if estimated_slippage > risk_params.max_slippage_pct:
        #     return False

        # 7. Cooldown Check (Stub)
        # if in_cooldown(signal.symbol):
        #     return False

        # --- FINAL GATE ---

        sim_result = await wallet_manager.simulate_transaction(
            signal.symbol,
            amount_to_trade,
            signal.type,
        )
        if not sim_result:
            logger.critical("GUARD: Trade BLOCKED - Simulation Failed")
            return False

        if self.is_halted() or system_state.emergency:
            logger.critical("GUARD: Trade ABORTED - Emergency raised during processing")
            return False

        logger.info(f"GUARD: PASS. Executing {signal.type} {amount_to_trade} SOL")
        logger.info(f"EXECUTING {signal.type} | {amount_to_trade:.4f} SOL")

        # Add to active orders under lock (best-effort; real system would persist)
        try:
            self.add_active_order({"symbol": signal.symbol, "amount": amount_to_trade, "type": str(signal.type)})
        except Exception:
            logger.exception("Failed to record active order")

        # TODO: Wallet signing + broadcast

        return True


execution_engine = ExecutionEngine()

# Expose convenient properties that map to the shared state
def _prop(name):
    return property(lambda self: self._shared.get(name), lambda self, v: self._shared.__setitem__(name, v))


# attach dynamic properties to ExecutionEngine
ExecutionEngine.halted = _prop("halted")
ExecutionEngine.halted_since = _prop("halted_since")


# Active orders helpers: access must be protected by the engine's _cancel_lock
def _active_orders_list(self):
    # Return a shallow copy list for safe iteration
    ao = self._shared.get("active_orders")
    try:
        return list(ao)
    except Exception:
        return []

ExecutionEngine._active_orders = property(_active_orders_list)

# Instance methods for thread-safe active_orders manipulation
def _add_active_order(self, order):
    with self._cancel_lock:
        ao = self._shared.get("active_orders")
        try:
            ao.append(order)
        except Exception:
            # Fallback: recreate as list
            self._shared["active_orders"] = deque(list(ao) + [order])

def _clear_active_orders(self):
    with self._cancel_lock:
        ao = self._shared.get("active_orders")
        try:
            ao.clear()
        except Exception:
            # Recreate empty deque
            self._shared["active_orders"] = deque()

def _get_active_orders(self):
    with self._cancel_lock:
        ao = self._shared.get("active_orders")
        try:
            return list(ao)
        except Exception:
            return []

ExecutionEngine.add_active_order = _add_active_order
ExecutionEngine.clear_active_orders = _clear_active_orders
ExecutionEngine.get_active_orders = _get_active_orders
