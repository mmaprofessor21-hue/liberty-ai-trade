// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./WalletDataBlock.css";

export default function WalletDataBlock() {
  return (
    <div className="wallet-data-terminal">
      <div className="wallet-tabs">
        <button className="tc-button">HOLDINGS</button>
        <button className="tc-button">HISTORY</button>
      </div>
      <pre className="wallet-terminal">
TOKEN     AMOUNT     P/L     TIMESTAMP
SOL       1.25       +42.10  10:22:01
BONK      500k       -18.44  10:21:10
WIF       220        +9.02   10:20:02
      </pre>
    </div>
  );
}
