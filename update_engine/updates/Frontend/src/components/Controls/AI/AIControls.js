// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
import React from "react";

import AIModeToggle from "./AIModeToggle";
import AIStrategySelector from "./AIStrategySelector";
import AIConfidenceSelector from "./AIConfidenceSelector";

export default function AIControls({
  aiEnabled,
  aiStrategy,
  aiConfidence,
  onToggleAI,
  onChangeAIStrategy,
  onChangeAIConfidence
}) {
  return (
    <div className="controls-section-block">
      <div className="controls-section-title">AI CONTROLS</div>

      <div className="controls-section-content">
        <AIModeToggle
          enabled={aiEnabled}
          onChange={onToggleAI}
        />

        <AIStrategySelector
          value={aiStrategy}
          onChange={onChangeAIStrategy}
        />

        <AIConfidenceSelector
          value={aiConfidence}
          onChange={onChangeAIConfidence}
        />
      </div>
    </div>
  );
}
