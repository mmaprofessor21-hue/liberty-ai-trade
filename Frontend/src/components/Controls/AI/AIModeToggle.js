import React from "react";

export default function AIModeToggle({ value, onChange }) {
  return (
    <div className="ai-controls">
      <div className="tc-label">AI MODE</div>
      <div className="tc-button-group">
        <button
          className={value === "AUTO" ? "active" : ""}
          aria-pressed={value === "AUTO"}
          data-intent="positive"
          onClick={() => onChange("AUTO")}
        >
          AUTO
        </button>
        <button
          className={value === "MANUAL" ? "active" : ""}
          aria-pressed={value === "MANUAL"}
          data-intent="positive"
          onClick={() => onChange("MANUAL")}
        >
          MANUAL
        </button>
        <button
          className={value === "OFF" ? "active" : ""}
          aria-pressed={value === "OFF"}
          data-intent="negative"
          onClick={() => onChange("OFF")}
        >
          OFF
        </button>
      </div>
    </div>
  );
}
