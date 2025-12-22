// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState } from "react";
import "./WalletControls.css";

export default function WalletLoggingMode() {
  const [mode, setMode] = useState("off");

  const handleOff = () => {
    if (mode === "off") return;
    setMode("off");
    // backend hook point (future)
  };

  const handleNormal = () => {
    if (mode === "normal") return;
    setMode("normal");
    // backend hook point (future)
  };

  const handleVerbose = () => {
    if (mode === "verbose") return;
    setMode("verbose");
    // backend hook point (future)
  };

  return (
    <div className="wallet-logging">
      <div className="controls-section-title">LOGGING MODE</div>

      <div className="tc-button-group">
        <button
          aria-pressed={mode === "off"}
          data-intent="negative"
          disabled={mode === "off"}
          onClick={handleOff}
        >
          OFF
        </button>

        <button
          aria-pressed={mode === "normal"}
          data-intent="positive"
          disabled={mode === "normal"}
          onClick={handleNormal}
        >
          NORMAL
        </button>

        <button
          aria-pressed={mode === "verbose"}
          data-intent="positive"
          disabled={mode === "verbose"}
          onClick={handleVerbose}
        >
          VERBOSE
        </button>
      </div>
    </div>
  );
}
