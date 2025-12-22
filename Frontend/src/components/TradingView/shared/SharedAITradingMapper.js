// Shared AI <-> Trading Mapper
export function mapAIToTrading(signal) {
    return {
        type: signal.type || "unknown",
        confidence: signal.confidence || 0,
        metadata: signal.metadata || {}
    };
}

export function mapTradingToAI(event) {
    return {
        action: event.action || "none",
        payload: event.payload || {}
    };
}
