// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE
/* TIMESTAMP PLACEHOLDER */

import React from "react";
import "./WalletControls.css";

import WalletStatus from "./WalletStatus/WalletStatus";
import WalletSecurityControls from "./WalletSecurityControls/WalletSecurityControls";
import WalletData from "./WalletData/WalletData";

export default function WalletControls() {
  return (
    <div className="wallet-section-container">
      {/* WALLET SECTION HEADER */}
      <div className="wallet-header-wrapper">
        <h2 className="wallet-title">WALLET</h2>
        <h3 className="wallet-subtitle">
          REAL-TIME WALLET STATUS, SECURITY & HOLDINGS POWERED BY LIBERTY AI TRADE
        </h3>
      </div>

      {/* WALLET CONTENT */}
      <div className="wallet-root">
        {/* WALLET STATUS */}
        <div className="wallet-section">
          <WalletStatus />
        </div>

        {/* WALLET SECURITY & CONTROLS */}
        <div className="wallet-section">
          <WalletSecurityControls />
        </div>

        {/* WALLET DATA */}
        <div className="wallet-section">
          <WalletData />
        </div>
      </div>
    </div>
  );
}
