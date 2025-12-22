
/**
 * PART 5C — AI PREDICTION ENGINE (SIMULATION LAYER)
 *
 * Backend will eventually feed REAL AI predictions here.
 * For now we simulate intelligent behavior based on:
 *   - token
 *   - strategy
 *   - sentiment score
 *   - strategy confidence
 */

export function generateAIPrediction(token, strategy, sentiment, strategyConf) {

    let type = "buy";
    let confidence = 50;

    // ------------------------
    // STRATEGY: CONTRARIAN SHORT MODE
    // ------------------------
    if (strategy === "Contrarian Short Mode") {
        if (sentiment > 65) {
            type = "sell";
            confidence = Math.min(60 + Math.floor(Math.random() * 30), 100);
        } else {
            type = "buy";
            confidence = 40 + Math.floor(Math.random() * 30);
        }
    }

    // ------------------------
    // STRATEGY: BULLISH ACCUMULATION
    // ------------------------
    if (strategy === "Bullish Accumulation Mode") {
        type = "buy";
        confidence = 65 + Math.floor(Math.random() * 25);
    }

    // ------------------------
    // STRATEGY: OVERSOLD LONG MODE
    // ------------------------
    if (strategy === "Oversold Long Mode") {
        if (sentiment < 35) {
            type = "buy";
            confidence = 70 + Math.floor(Math.random() * 20);
        } else {
            type = "sell";
            confidence = 40 + Math.floor(Math.random() * 25);
        }
    }

    const x = 0.88 + (Math.random() * 0.10);
    const y = 0.25 + (Math.random() * 0.50);

    return {
        type,
        token,
        confidence,
        strategy,
        strategyConf,
        x,
        y
    };
}
