// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./ControlsSection.css";
import ControlsPanel from "./ControlsPanel";

export default function ControlsSection() {
  return (
    <section className="controls-section">
      <div className="controls-section-inner">
        <h2 className="controls-title">CONTROLS</h2>
        <p className="controls-subtitle">
          Configure trading behaviors, AI logic, system actions, and wallet connectivity.
        </p>

        <ControlsPanel />
      </div>
    </section>
  );
}
