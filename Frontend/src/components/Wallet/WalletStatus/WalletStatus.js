// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./WalletStatus.css";

export default function WalletStatus() {
  return (
    <div className="wallet-status-root">
      <div className="wallet-section-title gold">WALLET STATUS</div>

      <div className="wallet-status-grid">
        <div>
          <div className="wallet-label">BALANCE</div>
          <div className="wallet-value green">$12,450.38</div>

          <div className="wallet-label">ADDRESS</div>
          <div className="wallet-value">7GkF...9Qx2</div>
        </div>

        <div>
          <div className="wallet-label">NETWORK</div>
          <div className="wallet-value">Solana</div>

          <div className="wallet-label">STATUS</div>
          <div className="wallet-value green">Connected</div>
        </div>
      </div>
    </div>
  );
}
