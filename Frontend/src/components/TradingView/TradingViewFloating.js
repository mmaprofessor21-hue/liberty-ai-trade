import React from "react";
import "./TradingViewFloating.css";

export default function TradingViewFloating({ children, onDock }) {
  return (
    <div className="tv-floating-window">
      <div className="tv-floating-header">
        <span>TRADINGVIEW — FLOATING ANALYTICS</span>
        <button className="tv-dock-btn" onClick={onDock}>DOCK</button>
      </div>
      <div className="tv-floating-body">
        {children}
      </div>
    </div>
  );
}
