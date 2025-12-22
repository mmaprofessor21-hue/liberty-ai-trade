// DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// NO IMPORT OVERRIDES | NO PATH ASSUMPTIONS | ABSOLUTE STRUCTURE COMPLIANCE

import React, { useRef } from "react";
import "./TradingViewDock.css";

export default function TradingViewDock({ children }) {
  const ref = useRef(null);

  return (
    <div className="tradingview-dock" ref={ref}>
      {children}
    </div>
  );
}
