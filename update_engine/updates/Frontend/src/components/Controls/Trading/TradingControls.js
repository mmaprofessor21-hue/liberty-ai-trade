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
        <TradingLoggingMode
          value={loggingMode}
          onChange={setLoggingMode}
        />

        <TradingSniping
          value={snipingMode}
          onChange={setSnipingMode}
        />

        <TradingRiskLevel
          value={riskLevel}
          onChange={setRiskLevel}
        />

        <TradingStrategy
          value={strategy}
          onChange={setStrategy}
        />
      </div>
    </div>
  );
}
