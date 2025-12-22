// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function TradingLoggingMode({ value, onChange }) {
  const modes = ["OFF", "NORMAL", "VERBOSE"];
  const current = String(value || "").toUpperCase();

  return (
    <div className="tc-logging">
      <div className="tc-label">LOGGING MODE</div>
      <div className="tc-button-group">
        {modes.map(mode => {
          const isOff = mode === "OFF";
          return (
            <button
              key={mode}
              aria-pressed={current === mode}
              data-intent={isOff ? "negative" : "positive"}
              onClick={() => onChange(mode)}
            >
              {mode}
            </button>
          );
        })}
      </div>
    </div>
  );
}
