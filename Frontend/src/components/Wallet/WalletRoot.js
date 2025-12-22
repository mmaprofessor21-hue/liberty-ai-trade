// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./WalletRoot.css";
import "./WalletBackground.css";

import WalletStatus from "./WalletStatus";
import WalletSecurityControls from "./WalletSecurityControls";
import WalletData from "./WalletData";

export default function WalletRoot() {
  return (
    <div className="wallet-background">
      <div className="wallet-root">
        <WalletStatus />
        <WalletSecurityControls />
        <WalletData />
      </div>
    </div>
  );
}
