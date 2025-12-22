from enum import Enum
from pydantic import BaseModel
import random

class MarketRegime(str, Enum):
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    VOLATILE = "VOLATILE"
    UNCERTAIN = "UNCERTAIN"

class AIAnalysis(BaseModel):
    regime: MarketRegime
    entry_confidence: float # 0.0 to 1.0
    anomaly_score: float # 0.0 to 1.0 (Low is good, High is bad)
    strategy_suggestion: str
    explanation: str

# --- MODEL STUBS ---
# In a real torch/sklearn env, these would load .pth/.pkl files

class MarketRegimeClassifier:
    def predict(self, market_data: dict) -> MarketRegime:
        # Heuristic stub
        # If price > EMA, Trending. If ATR high, Volatile.
        return MarketRegime.TRENDING # Mock

class EntryProbabilityModel:
    def predict(self, market_data: dict) -> float:
        # Mock confidence score
        return random.uniform(0.4, 0.95)

class AnomalyDetector:
    def detect(self, market_data: dict) -> float:
        # Returns anomaly probability
        return 0.05 # Low anomaly

