// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function TradingStrategy({ value, onChange }) {
  const strategies = ["STANDARD", "SCALP", "TREND", "RANGE", "AI"];
  const current = String(value || "").toUpperCase();

  return (
    <div className="tc-strategy">
      <div className="tc-label">STRATEGY</div>
      <div className="tc-button-group">
        {strategies.map(strategy => (
          <button
            key={strategy}
            aria-pressed={current === strategy}
            data-intent="positive"
            onClick={() => onChange(strategy)}
          >
            {strategy}
          </button>
        ))}
      </div>
    </div>
  );
}
