import React from "react";

export default function AIStrategySelector({ value, onChange }) {
  const strategies = ["MOMENTUM", "CONTRARIAN", "HYBRID"];

  return (
    <div className="ai-controls">
      <div className="tc-label">AI STRATEGY</div>
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
