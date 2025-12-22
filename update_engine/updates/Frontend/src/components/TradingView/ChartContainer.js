// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./ChartContainer.css";

export const TRADINGVIEW_CONTAINER_ID = "tradingview-chart";

export default function ChartContainer() {
  return (
    <div
      id={TRADINGVIEW_CONTAINER_ID}
      className="tradingview-chart-container"
    />
  );
}
