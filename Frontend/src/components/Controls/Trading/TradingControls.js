// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState } from "react";
import "./TradingControls.css";

import TradingLoggingMode from "./TradingLoggingMode";
import TradingRiskLevel from "./TradingRiskLevel";
import TradingSniping from "./TradingSniping";
import TradingStrategy from "./TradingStrategy";

export default function TradingControls() {
  const [loggingMode, setLoggingMode] = useState("NORMAL");
  const [riskLevel, setRiskLevel] = useState("MEDIUM");
  const [snipingMode, setSnipingMode] = useState(false);
  const [strategy, setStrategy] = useState("STANDARD");

  return (
    <div className="controls-section-block">
      <div className="controls-section-title">TRADING CONTROLS</div>

      <div className="controls-section-content">
        {/* Row 1, Col 1: LOGGING MODE */}
        <div className="control-group">
          <TradingLoggingMode value={loggingMode} onChange={setLoggingMode} />
        </div>

        {/* Row 1, Col 2: SNIPING MODE */}
        <div className="control-group">
          <TradingSniping value={snipingMode} onChange={setSnipingMode} />
        </div>

        {/* Row 2, Col 1: RISK LEVEL */}
        <div className="control-group">
          <TradingRiskLevel value={riskLevel} onChange={setRiskLevel} />
        </div>

        {/* Row 2, Col 2: STRATEGY */}
        <div className="control-group">
          <TradingStrategy value={strategy} onChange={setStrategy} />
        </div>
      </div>
    </div>
  );
}
