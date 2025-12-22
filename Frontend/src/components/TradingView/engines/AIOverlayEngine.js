
/**
 * PART 6B — AI Overlay Engine (Simulated)
 *
 * Backend ML model will later replace this logic.
 */

export function generateOverlayData(token, strategy, sentiment, strategyConf) {

    // Heatmap strength: 0–1
    const heat = sentiment / 100;

    // Trend cloud direction
    const trend = strategy === "Contrarian Short Mode"
        ? -1
        : strategy === "Oversold Long Mode"
            ? 1
            : sentiment > 50
                ? 1
                : -1;

    // Support/resistance strength
    const srStrength = Math.min(1, strategyConf / 100);

    return {
        heat,
        trend,
        srStrength
    };
}
