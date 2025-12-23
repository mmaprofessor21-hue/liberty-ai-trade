// 🚨 WALLET SECURITY — FINAL ALIGNED VERSION

import React, { useState } from "react";
import "./WalletSecurityControls.css";

export default function WalletSecurityControls() {
  const [connection, setConnection] = useState("connect");
  // `secure` is currently a read-only indicator; use a plain constant to avoid unused-setter lint warnings
  const secure = true;

  return (
    <div className="wallet-security-root wallet-security-controls">

      <div className="wallet-section-title wallet-security-title">
        WALLET SECURITY & CONTROLS
      </div>

      <div className="wallet-security-grid">

        {/* LEFT COLUMN */}
        <div className="wallet-security-block">
          <div className="wallet-label">CONNECTION</div>
          <div className="wallet-btn-group">
            <button
              type="button"
              className="wallet-btn"
              data-intent="positive"
              aria-pressed={connection === "connect"}
              onClick={() => setConnection("connect")}
            >
              CONNECT
            </button>
            <button
              type="button"
              className="wallet-btn"
              data-intent="negative"
              aria-pressed={connection === "disconnect"}
              onClick={() => setConnection("disconnect")}
            >
              DISCONNECT
            </button>
          </div>

          <div className="wallet-label" style={{ marginTop: "14px" }}>
            FUNDS
          </div>
          <div className="wallet-btn-group">
            <button type="button" className="wallet-btn" data-intent="neutral">DEPOSIT</button>
            <button type="button" className="wallet-btn" data-intent="neutral">WITHDRAW</button>
          </div>
        </div>

        {/* RIGHT COLUMN — SECURITY CHECK */}
        <div className="wallet-security-block right">
          <div className="wallet-label">SECURITY CHECK</div>
          <div className="wallet-security-leds">
            <div className={"wallet-led safe" + (secure ? " active" : "")}></div>
            <span>SAFE</span>
            <div className={"wallet-led unsafe" + (!secure ? " active" : "")}></div>
            <span>UNSAFE</span>
          </div>
        </div>

      </div>
    </div>
  );
}
