// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./ControlsSection.css";
import ControlsPanel from "./ControlsPanel";

export default function ControlsSection({ aiMode, setAiMode }) {
  return (
    <div className="controls-section-container">
      {/* CONTROLS SECTION HEADER */}
      <div className="controls-header-wrapper">
        <h2 className="controls-title">CONTROLS</h2>
        <h3 className="controls-subtitle">
          CONFIGURE TRADING BEHAVIORS, AI LOGIC, SYSTEM ACTIONS, AND WALLET CONNECTIVITY.
        </h3>
      </div>

      {/* CONTROLS CONTENT */}
      <div className="controls-content-wrapper">
        <ControlsPanel aiMode={aiMode} setAiMode={setAiMode} />
      </div>
    </div>
  );
}
