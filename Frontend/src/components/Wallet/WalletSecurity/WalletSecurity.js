// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./WalletSecurity.css";

export default function WalletSecurity() {
  return (
    <div className="wallet-security-grid">
      <div className="wallet-actions">
        <button className="trading-btn">CONNECT</button>
        <button className="trading-btn disabled">DISCONNECT</button>
        <button className="trading-btn">DEPOSIT</button>
        <button className="trading-btn">WITHDRAW</button>
      </div>

      <div className="wallet-security-check">
        <div className="wallet-label">SECURITY CHECK</div>
        <div className="security-led safe">SAFE</div>
        <div className="security-led unsafe">UNSAFE</div>
      </div>
    </div>
  );
}
