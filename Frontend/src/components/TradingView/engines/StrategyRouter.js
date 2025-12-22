
/**
 * PART 5A — AI STRATEGY ROUTER
 *
 * This engine receives:
 *   - token (SOL, BTC, XRP…)
 *   - sentiment score
 *   - future market conditions (placeholder)
 *   - user AI mode (optional future)
 *
 * And returns the AI strategy currently active.
 *
 * NOTE:
 * This routing architecture is required for future modules:
 *   - Leverage AI
 *   - Short AI
 *   - Arbitrage AI
 *   - Pattern recognition AI
 */

export function getActiveStrategy(token, sentiment) {

    let strategy = "Neutral Mode";
    let confidence = 50;

    // ---------------------------
    // Contrarian Mode (requested by you earlier)
    // ---------------------------
    if (sentiment >= 70) {
        strategy = "Contrarian Short Mode";
        confidence = 70 + Math.floor(Math.random() * 20);
    }

    // ---------------------------
    // Bullish Accumulation
    // ---------------------------
    if (sentiment >= 40 && sentiment < 70) {
        strategy = "Bullish Accumulation Mode";
        confidence = 60 + Math.floor(Math.random() * 20);
    }

    // ---------------------------
    // Oversold / Long Trigger
    // ---------------------------
    if (sentiment < 40) {
        strategy = "Oversold Long Mode";
        confidence = 60 + Math.floor(Math.random() * 20);
    }

    // ---------------------------
    // Token-specific overrides (foundation only)
    // ---------------------------
    if (token === "BTC") {
        confidence += 5;
    }

    if (token === "SOL") {
        confidence += 3;
    }

    return {
        strategy,
        confidence: Math.min(confidence, 100)
    };
}
