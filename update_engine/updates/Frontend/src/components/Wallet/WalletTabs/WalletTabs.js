import React from "react";
import "./WalletTabs.css";

export default function WalletTabs({ activeTab, setActiveTab }) {
  return (
    <div className="wallet-tabs">
      <div
        className={`wallet-tab ${activeTab === "holdings" ? "wallet-tab-active" : ""}`}
        onClick={() => setActiveTab("holdings")}
      >
        HOLDINGS
      </div>
      <div
        className={`wallet-tab ${activeTab === "history" ? "wallet-tab-active" : ""}`}
        onClick={() => setActiveTab("history")}
      >
        HISTORY
      </div>
    </div>
  );
}
