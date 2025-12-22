from core.control_router import RiskLevel
from pydantic import BaseModel

class TradeRisk(BaseModel):
    max_position_size_sol: float
    stop_loss_pct: float
    take_profit_pct: float
    max_slippage_pct: float

class RiskEngine:
    def __init__(self):
        pass

    def get_risk_parameters(self, level: RiskLevel, balance: float) -> TradeRisk:
        """
        Calculates position sizing and safe-guards based on Risk Level and Wallet Balance.
        """
        if level == RiskLevel.LOW:
            # Conservative: 5% of balance, tight safety, wide profit
            return TradeRisk(
                max_position_size_sol=balance * 0.05,
                stop_loss_pct=0.02,  # 2% SL
                take_profit_pct=0.05, # 5% TP
                max_slippage_pct=0.005 # 0.5%
            )
        elif level == RiskLevel.MEDIUM:
            # Balanced: 10% of balance
            return TradeRisk(
                max_position_size_sol=balance * 0.10,
                stop_loss_pct=0.05,
                take_profit_pct=0.10,
                max_slippage_pct=0.01
            )
        elif level == RiskLevel.HIGH:
            # Aggressive: 25% of balance, wider stops for volatility
            return TradeRisk(
                max_position_size_sol=balance * 0.25,
                stop_loss_pct=0.10,
                take_profit_pct=0.20,
                max_slippage_pct=0.02
            )
        else:
            # Default to LOW safety
            return TradeRisk(
                max_position_size_sol=balance * 0.01,
                stop_loss_pct=0.01,
                take_profit_pct=0.02,
                max_slippage_pct=0.005
            )

    def validate_trade(self, amount: float, risk_params: TradeRisk) -> bool:
        """
        Rejects trades that violate risk caps.
        """
        if amount > risk_params.max_position_size_sol:
            return False
        return True

risk_engine = RiskEngine()
