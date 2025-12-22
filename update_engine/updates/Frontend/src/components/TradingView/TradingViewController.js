// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE
// TIMESTAMP: 2025-12-21_15-01-22

import React from "react";
import TradingViewChartSection from "./TradingViewChartSection";
import "./TradingViewController.css";

export default function TradingViewController() {
  return (
    <section
      className="tradingview-controller-root"
      style={
        position: "relative",
        width: "100%",
        height: "auto",
        minHeight: "520px",
        overflow: "visible",
      }
    >
      <TradingViewChartSection />
    </section>
  );
}
