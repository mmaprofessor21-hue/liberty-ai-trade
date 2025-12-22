// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
import React from "react";
import "./AIControls.css";

import AIModeToggle from "./AIModeToggle";
import AIStrategySelector from "./AIStrategySelector";
import AIConfidenceSelector from "./AIConfidenceSelector";

export default function AIControls({ aiMode, setAiMode }) {
  const [aiStrategy, setAiStrategy] = React.useState("MOMENTUM");
  const [aiConfidence, setAiConfidence] = React.useState("MEDIUM");

  return (
    <div className="controls-section-block">
      <div className="controls-section-title">AI CONTROLS</div>

      <div className="controls-section-content">
        <AIModeToggle
          value={aiMode}
          onChange={setAiMode}
        />

        <AIStrategySelector
          value={aiStrategy}
          onChange={setAiStrategy}
        />

        <AIConfidenceSelector
          value={aiConfidence}
          onChange={setAiConfidence}
        />
      </div>
    </div>
  );
}
