
/**
 * PART 6A — AI EXPLANATION ENGINE (SIMULATION)
 *
 * Backend will later replace this module with actual model output.
 */

export function generateAIExplanation(token, strategy, sentiment, strategyConf) {

    let summary = "";

    if (strategy === "Contrarian Short Mode") {
        summary = `Market sentiment appears overheated for ${token}. AI is positioning against excessive bullishness.`;
    }

    if (strategy === "Bullish Accumulation Mode") {
        summary = `Moderate sentiment indicates a healthy accumulation environment for ${token}. AI expects upward continuation.`;
    }

    if (strategy === "Oversold Long Mode") {
        summary = `${token} sentiment is showing signs of exhaustion. AI expects a relief bounce or trend reversal.`;
    }

    const pattern = sentiment > 65
        ? "Detected: Overbought Momentum"
        : sentiment < 35
            ? "Detected: Oversold Weakness"
            : "Detected: Neutral Pattern Structure";

    return {
        summary,
        pattern,
        sentiment,
        strategy,
        strategyConf
    };
}
