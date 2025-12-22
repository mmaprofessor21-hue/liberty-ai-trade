// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function WalletStatusBlock({ balance = "—", address = "—", network = "Solana", status = "DISCONNECTED" }) {
  return (
    <div className="wallet-block wallet-status-block">
      <h4 className="wallet-block-title">WALLET STATUS</h4>

      <div className="wallet-status-grid">
        <div className="wallet-status-col">
          <div className="wallet-status-row">
            <div className="wallet-status-label">BALANCE</div>
            <div className="wallet-status-value">{balance}</div>
          </div>

          <div className="wallet-status-row">
            <div className="wallet-status-label">ADDRESS</div>
            <div className="wallet-status-value wallet-mono">{address}</div>
          </div>
        </div>

        <div className="wallet-status-col">
          <div className="wallet-status-row">
            <div className="wallet-status-label">NETWORK</div>
            <div className="wallet-status-value">{network}</div>
          </div>

          <div className="wallet-status-row">
            <div className="wallet-status-label">STATUS</div>
            <div className="wallet-status-value">{status}</div>
          </div>
        </div>
      </div>

    </div>
  );
}
