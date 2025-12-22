import React from "react";

export default function AIConfidenceSelector({ value, onChange }) {
  const levels = ["LOW", "MEDIUM", "HIGH"];

  return (
    <div className="ai-controls">
      <div className="tc-label">AI CONFIDENCE</div>
      <div className="tc-button-group">
        {levels.map(level => (
          <button
            key={level}
            aria-pressed={value === level}
            onClick={() => onChange(level)}
          >
            {level}
          </button>
        ))}
      </div>
    </div>
  );
}
