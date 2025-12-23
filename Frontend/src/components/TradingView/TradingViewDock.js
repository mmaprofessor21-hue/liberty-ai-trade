// DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// NO IMPORT OVERRIDES | NO PATH ASSUMPTIONS | ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./TradingViewDock.css";

const TradingViewDock = React.memo(function TradingViewDock({ children }) {
  return (
    <div className="dock-wrapper" style={{ position: "relative" }}>
      {children || null}
    </div>
  );
});

export default TradingViewDock;
