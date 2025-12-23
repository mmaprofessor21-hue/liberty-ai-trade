// DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// NO IMPORT OVERRIDES | NO PATH ASSUMPTIONS | ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./TradingViewDock.css";

export default function TradingViewDock({ children }) {
  return (
    <div className="dock-wrapper" style={{ position: "relative" }}>
      {children}
    </div>
  );
}
