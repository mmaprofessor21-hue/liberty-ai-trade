// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState } from "react";
import "./BotSystemActions.css";

export default function BotSystemActions() {
  const [botStatus, setBotStatus] = useState("STOPPED");
  const [isEmergency, setIsEmergency] = useState(false);

  const handleAction = (status) => {
    setIsEmergency(false); // Reset emergency if any other action is taken
    setBotStatus(status);
  };

  const handleEmergencyStop = () => {
    console.log("EMERGENCY STOP TRIGGERED - Connecting to backend...");
    setIsEmergency(true);
    setBotStatus("STOPPED");
  };

  return (
    <div className="system-controls-root">

      {/* SYSTEM STATUS */}
      <div className="system-block">
        <h4>SYSTEM STATUS</h4>
        <div className="status-line">
          <span>Status</span>
          <span className={`led ${isEmergency ? "red high-priority" : botStatus === "RUNNING" || botStatus === "RESTARTED" ? "green" : botStatus === "PAUSED" ? "orange" : "red"} glow`}>
            {isEmergency ? "EMERGENCY STOP" : botStatus}
          </span>
        </div>
        <div className="status-line">
          <span>Execution Mode</span>
          <span>REMOTE (Telegram)</span>
        </div>
        <div className="status-line">
          <span>Last Action</span>
          <span>STOP</span>
        </div>
      </div>

      {/* CONTROL AUTHORITY */}
      <div className="system-block">
        <h4>CONTROL AUTHORITY</h4>
        <div className="status-line">
          <span>Local Control</span>
          <span className="led green glow">ACTIVE</span>
        </div>
        <div className="status-line">
          <span>Telegram Control</span>
          <span className="led green glow">ENABLED</span>
        </div>
        <div className="status-line">
          <span>Scope</span>
          <span>FULL CONTROL</span>
        </div>
        <div className="status-line">
          <span>Last Remote Cmd</span>
          <span>@telegram_admin • START</span>
        </div>
      </div>

      {/* SYSTEM HEALTH */}
      <div className="system-block">
        <h4>SYSTEM HEALTH</h4>
        <div className="status-line">
          <span>Frontend</span>
          <span className="led green glow">ONLINE</span>
        </div>
        <div className="status-line">
          <span>Backend</span>
          <span className="led green glow">CONNECTED</span>
        </div>
        <div className="status-line">
          <span>Trading Engine</span>
          <span className="led green glow">ACTIVE</span>
        </div>
        <div className="status-line">
          <span>Wallet Secure</span>
          <span className="led green glow">ISOLATED</span>
        </div>
        <div className="status-line">
          <span>Security Check</span>
          <span className="led green glow">OK</span>
        </div>
        <div className="status-line">
          <span>Network</span>
          <span className="led green glow">SOLANA</span>
        </div>
        <div className="status-line">
          <span>Data Feed</span>
          <span className="led green glow">LIVE</span>
        </div>
      </div>

      {/* ACTIONS */}
      <div className="system-block actions">
        <h4>ACTIONS</h4>
        <div className="action-row">
          <button
            aria-pressed={botStatus === "RUNNING" && !isEmergency}
            data-intent="positive"
            onClick={() => handleAction("RUNNING")}
          >
            Start
          </button>
          <button
            aria-pressed={botStatus === "STOPPED" && !isEmergency}
            data-intent="negative"
            onClick={() => handleAction("STOPPED")}
          >
            Stop
          </button>
          <button
            aria-pressed={botStatus === "RESTARTED" && !isEmergency}
            data-intent="positive"
            onClick={() => handleAction("RESTARTED")}
          >
            Restart
          </button>
          <button
            aria-pressed={botStatus === "PAUSED" && !isEmergency}
            data-intent="negative"
            onClick={() => handleAction("PAUSED")}
          >
            Pause
          </button>
        </div>
      </div>

      {/* EMERGENCY */}
      <div className="system-block emergency">
        <h4>EMERGENCY</h4>
        <button
          className={`emergency-btn ${isEmergency ? "active" : ""}`}
          onClick={handleEmergencyStop}
        >
          {isEmergency ? "SYSTEM HALTED" : "EMERGENCY STOP"}
        </button>
      </div>

    </div>
  );
}
