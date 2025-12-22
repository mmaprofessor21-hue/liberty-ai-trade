// DO NOT MODIFY OUTSIDE README_UPDATER RULES
/* TIMESTAMP: 2025-12-21_15-01-22 */

import React from 'react';
import './PerformancePanel.css';
import KPIItem from './KPIItem';
import icons from './PerformanceIcons';

export default function PerformancePanel() {

  const KPIS = [
    { label: "PnL (USD)", value: "$0.00", icon: icons.pnlUsd },
    { label: "PnL (SOL)", value: "0.00 SOL", icon: icons.pnlSol },
    { label: "Win Rate (%)", value: "0%", icon: icons.winRate },
    { label: "Total Trades", value: "0", icon: icons.totalTrades },
    { label: "Last Trade Profit", value: "$0.00", icon: icons.lastProfit },
    { label: "Bot Uptime", value: "0h 00m", icon: icons.uptime },
    { label: "Trade Speed (TPS)", value: "0 TPS", icon: icons.tps },
    { label: "Strategy Mode", value: "N/A", icon: icons.strategy },
    { label: "Risk Level", value: "N/A", icon: icons.risk },
    { label: "Market Sentiment", value: "Neutral", icon: icons.sentiment },
    { label: "AI Confidence", value: "0%", icon: icons.aiConfidence }
  ];

  return (
    <div className="performance-container fade-in">

      <div className="top-title-divider"></div>

      <h2 className="perf-title">PERFORMANCE</h2>
      <h3 className="perf-subtitle">
        REAL-TIME METRICS POWERED BY LIBERTY AI TRADE ENGINE
      </h3>

      <div className="kpi-grid">
        {KPIS.map((item, idx) => (
          <KPIItem
            key={idx}
            label={item.label}
            value={item.value}
            icon={item.icon}
          />
        ))}
      </div>

      <div className="bottom-kpi-divider"></div>
    </div>
  );
}
