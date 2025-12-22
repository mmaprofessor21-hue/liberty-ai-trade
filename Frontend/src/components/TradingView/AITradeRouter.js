
/**
 * PART 5B — AI TRADE ROUTER
 *
 * This takes a BUY or SELL request and adapts output
 * according to the active strategy.
 *
 * Returns marker styling & metadata.
 */

export function routeAITrade(type, strategy, sentiment, token, strategyConf) {

    let color = "#00ff99";
    let glow = "#00ff99aa";
    let size = 12;

    // ---------------------
    // STRATEGY: CONTRARIAN SHORT MODE
    // ---------------------
    if (strategy === "Contrarian Short Mode") {
        if (type === "sell") {
            color = "#ff3333";
            glow = "#ff333399";
            size = 14;
        } else {
            color = "#ffaa00";
            glow = "#ffaa00aa";
            size = 10;
        }
    }

    // ---------------------
    // STRATEGY: BULLISH ACCUMULATION
    // ---------------------
    if (strategy === "Bullish Accumulation Mode") {
        if (type === "buy") {
            color = "#00ffcc";
            glow = "#00ffccaa";
            size = 14;
        } else {
            color = "#ccccff";
            glow = "#ccccffaa";
            size = 10;
        }
    }

    // ---------------------
    // STRATEGY: OVERSOLD LONG MODE
    // ---------------------
    if (strategy === "Oversold Long Mode") {
        if (type === "buy") {
            color = "#33ff77";
            glow = "#33ff77aa";
            size = 16;
        } else {
            color = "#ffaa00";
            glow = "#ffaa00aa";
            size = 10;
        }
    }

    // ---------------------
    // UNIVERSAL META
    // ---------------------
    return {
        type,
        token,
        sentiment,
        strategy,
        strategyConf,
        style: { color, glow, size }
    };
}
