from core.control_router import ai_state, AIConfidence
from ai.models import MarketRegimeClassifier, EntryProbabilityModel, AnomalyDetector, AIAnalysis, MarketRegime
import logging

logger = logging.getLogger(__name__)

class AIEngine:
    def __init__(self):
        self.regime_model = MarketRegimeClassifier()
        self.entry_model = EntryProbabilityModel()
        self.anomaly_models = AnomalyDetector()

    def analyze_market(self, market_data: dict) -> AIAnalysis:
        """
        Runs all models and aggregates results into an explainable analysis.
        """
        regime = self.regime_model.predict(market_data)
        confidence = self.entry_model.predict(market_data)
        anomaly = self.anomaly_models.detect(market_data)

        # Explainability Logic
        explanation = f"Market is {regime.value}. Confidence {confidence:.2f} based on momentum. Anomaly score {anomaly:.2f}."
        
        # Adjust confidence based on anomaly (Security: Reduce confidence if anomaly high)
        if anomaly > 0.5:
            confidence *= 0.5
            explanation += " PENALIZED by Anomaly Detector."

        return AIAnalysis(
            regime=regime,
            entry_confidence=confidence,
            anomaly_score=anomaly,
            strategy_suggestion="MOMENTUM" if regime == MarketRegime.TRENDING else "MEAN_REVERSION",
            explanation=explanation
        )

    def should_trade(self, analysis: AIAnalysis) -> bool:
        """
        Gating Logic based on AI Confidence Threshold.
        """
        threshold = 0.5
        if ai_state.confidence_threshold == AIConfidence.LOW:
            threshold = 0.4
        elif ai_state.confidence_threshold == AIConfidence.MEDIUM:
            threshold = 0.6
        elif ai_state.confidence_threshold == AIConfidence.HIGH:
            threshold = 0.8
            
        is_allowed = analysis.entry_confidence >= threshold
        
        if not is_allowed:
            logger.info(f"AI Gating: Blocked. Conf {analysis.entry_confidence:.2f} < Threshold {threshold}")
            
        return is_allowed

ai_engine = AIEngine()
