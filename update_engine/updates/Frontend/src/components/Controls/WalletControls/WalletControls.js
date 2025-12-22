
import React from "react";
import "./WalletControls.css";

import WalletStatus from "./WalletStatus/WalletStatus";
import WalletSecurity from "./WalletSecurity/WalletSecurity";
// WalletData intentionally NOT touched in this bulk

export default function WalletControls() {
  return (
    <div className="wallet-root">
      <div className="wallet-section wallet-status-container">
        <WalletStatus />
      </div>

      <div className="wallet-section wallet-security-container">
        <WalletSecurity />
      </div>

      {/* Wallet Data intentionally excluded from this bulk */}
    </div>
  );
}
