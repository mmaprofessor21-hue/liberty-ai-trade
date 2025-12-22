// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./ControlsPanel.css";

import TradingControls from "./Trading/TradingControls";
import AIControls from "./AI/AIControls";
import BotSystemActions from "./System/BotSystemActions";

export default function ControlsPanel({ aiMode, setAiMode }) {
  return (
    <div className="controls-grid">

      <div className="controls-quadrant top-left">
        <TradingControls />
      </div>

      <div className="controls-quadrant top-right">
        <AIControls aiMode={aiMode} setAiMode={setAiMode} />
      </div>

      <div className="controls-quadrant bottom-left">
        <BotSystemActions />
      </div>

    </div>
  );
}
