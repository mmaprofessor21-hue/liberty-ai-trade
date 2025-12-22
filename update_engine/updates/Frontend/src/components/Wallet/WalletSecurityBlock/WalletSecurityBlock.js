// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function WalletSecurityBlock({ status = "UNSAFE" }) {
  const normalized = String(status || "").toUpperCase();
  const isSafe = normalized === "SAFE" || normalized === "SECURE";
  const label = isSafe ? "SECURE" : "UNSAFE";

  return (
    <div className="wallet-block wallet-security-block">
      <h4 className="wallet-block-title">WALLET SECURITY</h4>

      <div className="wallet-security-row">
        <div className={`wallet-security-led ${isSafe ? "wallet-led-safe" : "wallet-led-unsafe"}`}>
          {label}
        </div>
        <div className="wallet-security-note">Security Check</div>
      </div>

    </div>
  );
}
