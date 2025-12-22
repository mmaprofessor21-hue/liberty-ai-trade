import React from "react";

export default function AIModeToggle({ enabled, onToggle }) {
  return (
    <div className="ai-controls">
      <div className="tc-label">AI MODE</div>
      <div className="tc-button-group">
        <button
          aria-pressed={enabled === true}
          onClick={() => onToggle(true)}
        >
          ENABLED
        </button>
        <button
          aria-pressed={enabled === false}
          onClick={() => onToggle(false)}
        >
          DISABLED
        </button>
      </div>
    </div>
  );
}
