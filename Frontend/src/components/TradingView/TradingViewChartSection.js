// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState, useEffect } from "react";
import { createTradingViewWidget } from "./TradingViewWidget";
import TradingViewMarkers from "./overlays/indicators/TradingViewMarkers";
import AIHeatmapOverlay from "./overlays/ai/AIHeatmapOverlay";
import AITendencyCloud from "./overlays/ai/AITendencyCloud";
import AISupportResistance from "./overlays/ai/AISupportResistance";
import TradingViewController from "./TradingViewController";
import TradingViewDock from "./TradingViewDock";
import TradingViewFloating from "./TradingViewFloating";
import { enableDrag } from "./DockManager";
import "./TradingViewChartSection.css";
import "./ChartContainer.css";

const TRADINGVIEW_CONTAINER_ID = "tradingview-chart-mount";

export default function TradingViewChartSection({ aiMode }) {
  const [docked, setDocked] = useState(true);
  const [chartHeight, setChartHeight] = useState(450); // Reduced from 600
  const [tradeAmount, setTradeAmount] = useState(100);
  const [overlays, setOverlays] = useState({
    scalping: true, trend: false, meanReversion: false,
    markers: true, zones: true, confidence: false,
    ema: true, vwap: false, sr: false, volume: true
  });

  const startVerticalResize = (e) => {
    e.preventDefault();
    const startY = e.clientY;
    const startHeight = chartHeight;

    const onMouseMove = (moveEvent) => {
      // Dragging UP decreases clientY, meaning a positive delta increases height
      const delta = startY - moveEvent.clientY;
      setChartHeight(Math.max(400, Math.min(1200, startHeight + delta)));
    };

    const onMouseUp = () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  };

  useEffect(() => {
    console.log(`[TradingViewChartSection] Effect initializing. Docked: ${docked} | Height: ${chartHeight}`);

    const timer = setTimeout(() => {
      const container = document.getElementById(TRADINGVIEW_CONTAINER_ID);
      if (!container) {
        console.warn(`[TradingViewChartSection] Container ${TRADINGVIEW_CONTAINER_ID} not found.`);
        return;
      }

      const widget = createTradingViewWidget({
        container: TRADINGVIEW_CONTAINER_ID,
        symbol: "BINANCE:BTCUSDT",
        interval: "15"
      });

      if (!docked) {
        const floatWindow = document.querySelector(".tv-floating-window");
        if (floatWindow) enableDrag(floatWindow);
      }

      return () => {
        if (widget && typeof widget.remove === "function") {
          console.log("[TradingViewChartSection] Widget cleanup.");
          widget.remove();
        }
      };
    }, 1200); // 1.2s delay for stabilization

    return () => clearTimeout(timer);
  }, [docked, aiMode]);

  const handleBuy = () => {
    console.log(`[EXECUTION] BUY Order placed for $${tradeAmount} BTCUSDT`);
    alert(`BUY Order Placed: $${tradeAmount} BTCUSDT`);
  };

  const handleSell = () => {
    console.log(`[EXECUTION] SELL Order placed for $${tradeAmount} BTCUSDT`);
    alert(`SELL Order Placed: $${tradeAmount} BTCUSDT`);
  };

  // --- WEBSOCKET INTEGRATION ---
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8080/ws/market_data");

    ws.onopen = () => {
      console.log("[WS] Connected to Market Data Stream");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "TRADE_EVENT") {
          console.log("[WS] Trade Event:", data);
          // Add new marker
          setMarkers(prev => [...prev, {
            type: data.action.toLowerCase(), // "buy" or "sell"
            x: Math.random(), // Mock X for demo (should be time/candle index)
            y: Math.random(), // Mock Y
            style: {
              size: 6,
              color: data.action === "BUY" ? "#00ffb2" : "#ff4d4d",
              glow: data.action === "BUY" ? "rgba(0, 255, 180, 0.4)" : "rgba(255, 80, 80, 0.4)"
            }
          }]);
        }
      } catch (err) {
        console.error("[WS] Error parsing message:", err);
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  const [markers, setMarkers] = useState([
    { type: "buy", x: 0.2, y: 0.3, style: { size: 6, color: "#00ffb2", glow: "rgba(0, 255, 180, 0.4)" } },
    { type: "sell", x: 0.5, y: 0.7, style: { size: 6, color: "#ff4d4d", glow: "rgba(255, 80, 80, 0.4)" } }
  ]);

  const renderContent = () => (
    <>
      <div className="tv-header-centered-wrapper">
        <div
          className="tv-resize-handle-top"
          onMouseDown={startVerticalResize}
          title="Drag up to expand chart"
        />

        <TradingViewController
          overlays={overlays}
          setOverlays={setOverlays}
          docked={docked}
          aiMode={aiMode}
          tradeAmount={tradeAmount}
          setTradeAmount={setTradeAmount}
          onBuy={handleBuy}
          onSell={handleSell}
          onUndock={() => {
            console.log("[TradingViewChartSection] Undocking requested.");
            setDocked(false);
          }}
        />
      </div>

      <div className="tv-chart-main-row" style={{ position: "relative", width: "100%", height: `${chartHeight}px`, transition: "height 0.1s ease-out" }}>
        <div id={TRADINGVIEW_CONTAINER_ID} className="tv-chart-container" style={{ height: "100%" }} />

        {/* VISUAL OVERLAY LAYERS — NOW CLEANLY LAYERED ON TOP OF CHART */}
        {overlays.markers && <TradingViewMarkers markers={markers} />}
        {overlays.zones && <AIHeatmapOverlay heat={0.6} />}
        {overlays.trend && <AITendencyCloud trend={1} />}
        {overlays.sr && <AISupportResistance strength={1} />}

        {/* TECHNICAL OVERLAYS (INDICATOR BRIDGES) */}
        {overlays.volume && <div className="tv-volume-bridge" style={{ position: "absolute", bottom: 0, height: "15%", width: "100%", background: "linear-gradient(to top, rgba(0, 200, 255, 0.05), transparent)", pointerEvents: "none" }} />}
      </div>
    </>
  );

  return (
    <section className="tradingview-chart-section">
      {docked ? (
        <TradingViewDock>
          {renderContent()}
        </TradingViewDock>
      ) : (
        <TradingViewFloating onDock={() => {
          console.log("[TradingViewChartSection] Docking requested.");
          setDocked(true);
        }}>
          {renderContent()}
        </TradingViewFloating>
      )}
    </section>
  );
}
