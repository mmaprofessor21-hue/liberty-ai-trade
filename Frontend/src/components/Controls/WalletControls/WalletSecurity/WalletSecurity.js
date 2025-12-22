// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState } from "react";
import "./WalletSecurity.css";

export default function WalletSecurity() {
  const [connected, setConnected] = useState(false);

  return (
    <div className="wallet-security-root">
      <div className="wallet-security-controls">

        <div className="tc-label">CONNECTION</div>
        <div className="tc-button-group">
          <button
            className="tc-button"
            aria-pressed={connected}
            data-intent="positive"
            onClick={() => setConnected(true)}
          >
            CONNECT
          </button>
          <button
            className="tc-button"
            aria-pressed={!connected}
            data-intent="negative"
            onClick={() => setConnected(false)}
          >
            DISCONNECT
          </button>
        </div>

        <div className="tc-label">FUNDS</div>
        <div className="tc-button-group">
          <button className="tc-button" data-intent="positive">
            DEPOSIT
          </button>
          <button className="tc-button" data-intent="negative">
            WITHDRAW
          </button>
        </div>

      </div>
    </div>
  );
}
