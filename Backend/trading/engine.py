from core.control_router import Strategy, trading_state
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class TradeSignal(BaseModel):
    type: SignalType
    symbol: str
    price: float
    feature_values: dict  # Interpreted by Execution/Logs
    strategy: str
    ai_confidence: Optional[float] = 0.0
    ai_explanation: Optional[str] = "No AI Analysis"

class TradingEngine:
    def __init__(self):
        # In a real system, we'd initialize strategy classes here
        pass

    def evaluate_tick(self, tick_data: dict) -> Optional[TradeSignal]:
        """
        Main loop hook. Receives market data, checks active strategy, returns Signal.
        """
        current_strategy = trading_state.strategy
        
        # Dispatch to specific strategy logic
        if current_strategy == Strategy.STANDARD:
            return self._strategy_standard(tick_data)
        elif current_strategy == Strategy.SCALP:
            return self._strategy_scalp(tick_data)
        elif current_strategy == Strategy.TREND:
            return self._strategy_trend(tick_data)
        elif current_strategy == Strategy.RANGE:
            return self._strategy_range(tick_data)
        elif current_strategy == Strategy.AI:
            return self._strategy_ai(tick_data)
            
        return None

    def _strategy_standard(self, data):
        # Stub: EMA crossover logic would go here
        # For now, return HOLD
        return None

    def _strategy_scalp(self, data):
        # Stub: Momentum logic
        return None
        
    def _strategy_trend(self, data):
        # Stub: Higher TF bias
        return None
        
    def _strategy_range(self, data):
        # Stub: Mean reversion
        return None
        
    def _strategy_ai(self, data):
        """
        AI-Driven Strategy.
        1. Calls AI Engine for analysis.
        2. Checks if confidence allows trading.
        3. Returns Signal if valid.
        """
        from ai.engine import ai_engine, AIAnalysis
        
        # Mock market data needed for AI
        market_data = {"price": data.get("price", 0), "volume": 1000} 
        
        analysis: AIAnalysis = ai_engine.analyze_market(market_data)
        
        # We assume Trading Engine respects AI opinion, 
        # but Execution Engine is the final guard.
        # We pass the signal along with confidence.
        
        if ai_engine.should_trade(analysis):  # Optimization: filter early if low confidence
             return TradeSignal(
                 type=SignalType.BUY, # Mock direction for now
                 symbol=data.get("symbol", "SOL/USDC"),
                 price=data.get("price", 0),
                 feature_values={},
                 strategy="AI",
                 ai_confidence=analysis.entry_confidence,
                 ai_explanation=analysis.explanation
             )
        
        return None

trading_engine = TradingEngine()
