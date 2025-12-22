import React from "react";

export default function TradingSnipingMode({ enabled, onToggle }) {
  return (
    <div className="trading-controls">
      <div className="tc-label">SNIPING MODE</div>
      <div className="tc-button-group">
        <button
          aria-pressed={enabled === true}
          onClick={() => onToggle(true)}
        >
          ON
        </button>
        <button
          aria-pressed={enabled === false}
          onClick={() => onToggle(false)}
        >
          OFF
        </button>
      </div>
    </div>
  );
}
