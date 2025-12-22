import React from "react";

export default function TradingStrategySelector({ value, onChange }) {
  const strategies = ["STANDARD", "SCALP", "TREND", "RANGE", "AI"];

  return (
    <div className="trading-controls">
      <div className="tc-label">STRATEGY</div>
      <div className="tc-button-group">
        {strategies.map(strategy => (
          <button
            key={strategy}
            aria-pressed={value === strategy}
            onClick={() => onChange(strategy)}
          >
            {strategy}
          </button>
        ))}
      </div>
    </div>
  );
}
