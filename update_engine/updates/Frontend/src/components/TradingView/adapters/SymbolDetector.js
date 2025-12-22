
import React, { useEffect } from "react";
import { resolveToken } from "./TokenRouter";

export default function SymbolDetector({ onResolve }) {

    useEffect(() => {
        const scan = () => {
            try {
                const nodes = Array.from(document.querySelectorAll("span, div"))
                    .map(el => el.textContent)
                    .filter(t => t && t.includes("/"));

                const structured = nodes.map(n => ({
                    raw: n.trim(),
                    type: "detector"
                }));

                const result = resolveToken(structured);
                if (result && result.token) onResolve(result);

            } catch (err) {
                console.warn("SymbolDetector error:", err);
            }
        };

        scan();
        const id = setInterval(scan, 2500);

        return () => clearInterval(id);
    }, [onResolve]);

    return null;
}
