// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import ChartContainer from "./ChartContainer";
import TradingViewController from "./TradingViewController";
import "./TradingViewChartSection.css";

export default function TradingViewChartSection() {
  return (
    <section className="tradingview-section">
      <ChartContainer />
      <TradingViewController />
    </section>
  );
}
