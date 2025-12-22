// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React from "react";
import "./TradingViewController.css";

export default function TradingViewController({ overlays, setOverlays, docked, onUndock, aiMode, tradeAmount, setTradeAmount, onBuy, onSell }) {

  const toggleOverlay = (key) => {
    setOverlays(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="tv-overlay">
      <div className="tv-overlay-row tv-overlay-row-metrics">
        <div className="tv-overlay-label" style={{ color: "#00ffb2" }}>AI CONFIDENCE</div>
        <div className="tv-overlay-metric" style={{ color: "#00ffb2" }}>87%</div>
        {docked && (
          <button className="tv-undock-btn" onClick={onUndock} style={{ marginLeft: "auto" }}>UNDOCK</button>
        )}
      </div>

      <div className="tv-overlay-row tv-overlay-row-controls">
        <div className="tv-menu-section">
          <div className="tv-menu-title" style={{ color: "#d9b26d" }}>STRATEGY</div>
          <div className="tv-overlay-toggles">
            <button className={overlays.scalping ? "active" : ""} onClick={() => toggleOverlay("scalping")}>SCALPING</button>
            <button className={overlays.trend ? "active" : ""} onClick={() => toggleOverlay("trend")}>TREND</button>
            <button className={overlays.meanReversion ? "active" : ""} onClick={() => toggleOverlay("meanReversion")}>MEAN REV</button>
          </div>
        </div>

        <div className="tv-menu-section">
          <div className="tv-menu-title" style={{ color: "#d9b26d" }}>AI / BOT</div>
          <div className="tv-overlay-toggles">
            <button className={overlays.markers ? "active" : ""} onClick={() => toggleOverlay("markers")}>MARKERS</button>
            <button className={overlays.zones ? "active" : ""} onClick={() => toggleOverlay("zones")}>ZONES</button>
            <button className={overlays.confidence ? "active" : ""} onClick={() => toggleOverlay("confidence")}>CONF BANDS</button>
          </div>
        </div>

        <div className="tv-menu-section">
          <div className="tv-menu-title" style={{ color: "#d9b26d" }}>TECHNICAL</div>
          <div className="tv-overlay-toggles">
            <button className={overlays.ema ? "active" : ""} onClick={() => toggleOverlay("ema")}>EMA/SMA</button>
            <button className={overlays.vwap ? "active" : ""} onClick={() => toggleOverlay("vwap")}>VWAP</button>
            <button className={overlays.sr ? "active" : ""} onClick={() => toggleOverlay("sr")}>S/R</button>
            <button className={overlays.volume ? "active" : ""} onClick={() => toggleOverlay("volume")}>VOLUME</button>
          </div>
        </div>
        {/* MOVING EXECUTION CONTROLS HERE FOR SINGLE ROW LAYOUT */}
        <div className={`tv-execution-group ${aiMode === 'AUTO' ? 'disabled' : ''}`} style={{ display: 'flex', gap: '32px', marginLeft: 'auto', flex: 1, justifyContent: 'flex-end' }}>

          <div className="tv-menu-section">
            <div className="tv-menu-title" style={{ color: "#d9b26d" }}>MANUAL EXECUTION</div>
            <div className="tv-execution-controls">
              <button
                className="tv-btn-buy"
                disabled={aiMode === 'AUTO'}
                onClick={onBuy}
              >
                BUY
              </button>
              <button
                className="tv-btn-sell"
                disabled={aiMode === 'AUTO'}
                onClick={onSell}
              >
                SELL
              </button>
            </div>
          </div>

          <div className="tv-menu-section" style={{ flex: 1, minWidth: '200px' }}>
            <div className="tv-menu-title" style={{ color: "#d9b26d" }}>TRADE AMOUNT ($)</div>
            <div className="tv-amount-slider-wrapper">
              <input
                type="range"
                min="10"
                max="1000"
                step="10"
                value={tradeAmount}
                onChange={(e) => setTradeAmount(e.target.value)}
                disabled={aiMode === 'AUTO'}
                className="tv-amount-slider"
              />
              <span className="tv-amount-display">${tradeAmount}</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
