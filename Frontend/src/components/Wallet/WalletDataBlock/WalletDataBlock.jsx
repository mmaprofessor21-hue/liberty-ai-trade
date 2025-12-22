
import React from "react";
import "./WalletDataBlock.css";

export default function WalletDataBlock({ children }) {
  return (
    <div className="wallet-block wallet-data-block">
      {children}
    </div>
  );
}
