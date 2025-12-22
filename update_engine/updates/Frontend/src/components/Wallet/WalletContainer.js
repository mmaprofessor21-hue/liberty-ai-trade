// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState } from "react";
import WalletControls from "./WalletControls";
import WalletLoggingMode from "./WalletLoggingMode";
import WalletStatus from "./WalletStatus";

export default function WalletContainer() {
  const [connected, setConnected] = useState(false);

  return (
    <>
      <WalletControls connected={connected} setConnected={setConnected} />
      <WalletLoggingMode />
      <WalletStatus connected={connected} />
    </>
  );
}
