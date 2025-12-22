// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function TradingSniping({ value, onChange }) {
  const isOn = value === true || value === "ON";

  return (
    <div className="tc-sniping">
      <div className="tc-label">SNIPING MODE</div>
      <div className="tc-button-group">
        <button
          aria-pressed={isOn}
          data-intent="positive"
          onClick={() => onChange(true)}
        >
          ON
        </button>
        <button
          aria-pressed={!isOn}
          data-intent="negative"
          onClick={() => onChange(false)}
        >
          OFF
        </button>
      </div>
    </div>
  );
}
