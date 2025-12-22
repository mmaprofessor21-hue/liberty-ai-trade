import React from "react";
import "./WalletLogging.css";

export default function WalletLogging({ loggingMode, setLoggingMode }) {
  return (
    <div className="wallet-section wallet-logging">
      <div className="wallet-label">Logging Mode</div>

      <div className="tc-button-group wallet-logging-buttons">
        <button
          type="button"
          aria-pressed={loggingMode === "off"}
          data-intent="negative"
          onClick={() => setLoggingMode("off")}
        >
          OFF
        </button>

        <button
          type="button"
          aria-pressed={loggingMode === "normal"}
          data-intent="positive"
          onClick={() => setLoggingMode("normal")}
        >
          NORMAL
        </button>

        <button
          type="button"
          aria-pressed={loggingMode === "verbose"}
          data-intent="positive"
          onClick={() => setLoggingMode("verbose")}
        >
          VERBOSE
        </button>
      </div>
    </div>
  );
}
