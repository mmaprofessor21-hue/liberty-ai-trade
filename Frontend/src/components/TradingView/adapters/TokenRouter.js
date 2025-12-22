
import { parseSymbol } from "./SymbolParser";

/**
 * PART 4D — TOKEN ROUTER
 * Collects results from Detector + Watcher + Parser
 * Scores them → selects the best token
 */

export function resolveToken(candidates) {
    let best = { token: null, score: 0 };

    candidates.forEach(entry => {
        if (!entry || !entry.raw) return;

        const parsed = parseSymbol(entry.raw);
        if (!parsed) return;

        let score = 60; // parser confidence base

        // Additional scoring
        if (entry.type === "mutation") score += 10;
        if (entry.type === "detector") score += 5;
        if (entry.raw.includes("/")) score += 10;
        if (entry.raw.includes("USD") || entry.raw.includes("USDT")) score += 5;

        if (score > best.score) {
            best = { token: parsed, score };
        }
    });

    return best;
}
