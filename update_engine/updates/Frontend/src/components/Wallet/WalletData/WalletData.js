// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./WalletData.css";

export default function WalletData() {
  return (
    <div className="wallet-data-terminal">
      <div className="wallet-label">WALLET DATA</div>

      <div className="wallet-tabs">
        <button className="trading-btn">HOLDINGS</button>
        <button className="trading-btn">HISTORY</button>
      </div>

      <pre className="wallet-terminal">
TOKEN   AMOUNT   P/L     TIME
SOL     1.25     +42.10  10:22
BONK    500k     -18.44  10:21
WIF     220      +9.02   10:20
      </pre>
    </div>
  );
}
