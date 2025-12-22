// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function TradingRiskLevel({ value, onChange }) {
  const levels = ["LOW", "MEDIUM", "HIGH"];
  const current = String(value || "").toUpperCase();

  return (
    <div className="tc-risk">
      <div className="tc-label">RISK LEVEL</div>
      <div className="tc-button-group">
        {levels.map(level => (
          <button
            key={level}
            aria-pressed={current === level}
            data-intent="positive"
            onClick={() => onChange(level)}
          >
            {level}
          </button>
        ))}
      </div>
    </div>
  );
}
