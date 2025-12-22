// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";

export default function WalletActionsBlock() {
  return (
    <div className="wallet-block wallet-actions-block">
      <h4 className="wallet-block-title">WALLET ACTIONS</h4>

      <div className="wallet-btn-row">
        <button type="button" data-action="momentary" data-intent="neutral">
          DEPOSIT
        </button>
        <button type="button" data-action="momentary" data-intent="neutral">
          WITHDRAW
        </button>
      </div>

    </div>
  );
}
