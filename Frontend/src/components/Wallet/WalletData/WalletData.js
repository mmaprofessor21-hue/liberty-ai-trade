// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE

import React, { useState, useEffect, useRef, useCallback } from "react";
import "./WalletData.css";
import WalletHoldings from "../WalletHoldings/WalletHoldings";
import WalletHistory from "../WalletHistory/WalletHistory";

export default function WalletData() {
  // --- STATE: LAYOUT & PERSISTENCE ---
  const [docked, setDocked] = useState(() => {
    const saved = localStorage.getItem("wallet-data-docked");
    return saved !== null ? JSON.parse(saved) : true;
  });

  const [floatingPos, setFloatingPos] = useState(() => {
    const saved = localStorage.getItem("wallet-data-pos");
    return saved ? JSON.parse(saved) : { x: 100, y: 100 };
  });

  const [floatingSize, setFloatingSize] = useState(() => {
    const saved = localStorage.getItem("wallet-data-size");
    return saved ? JSON.parse(saved) : { w: 900, h: 600 };
  });

  // --- STATE: CONTENT ---
  const [activeTab, setActiveTab] = useState(() => {
    return localStorage.getItem("wallet-data-tab") || "holdings";
  });

  const [filterText, setFilterText] = useState("");
  const [isRefreshing, setIsRefreshing] = useState(false);

  // --- REFS ---
  const panelRef = useRef(null);
  const dragRef = useRef(null);
  const isDragging = useRef(false);
  const isResizing = useRef(false);
  const dragOffset = useRef({ x: 0, y: 0 });
  const resizeStart = useRef({ x: 0, y: 0, w: 0, h: 0 });

  // --- EFFECTS: PERSISTENCE ---
  useEffect(() => {
    localStorage.setItem("wallet-data-docked", JSON.stringify(docked));
  }, [docked]);

  useEffect(() => {
    if (!docked) {
      localStorage.setItem("wallet-data-pos", JSON.stringify(floatingPos));
    }
  }, [floatingPos, docked]);

  useEffect(() => {
    if (!docked) {
      localStorage.setItem("wallet-data-size", JSON.stringify(floatingSize));
    }
  }, [floatingSize, docked]);

  useEffect(() => {
    localStorage.setItem("wallet-data-tab", activeTab);
  }, [activeTab]);

  // --- HANDLERS: DRAGGING ---
  const handleMouseDownDrag = (e) => {
    if (docked) return;
    if (e.target.closest("button") || e.target.closest("input")) return;

    isDragging.current = true;
    dragOffset.current = {
      x: e.clientX - floatingPos.x,
      y: e.clientY - floatingPos.y
    };

    document.addEventListener("mousemove", handleMouseMoveDrag);
    document.addEventListener("mouseup", handleMouseUpDrag);
    document.body.style.userSelect = "none";
  };

  const handleMouseMoveDrag = useCallback((e) => {
    if (!isDragging.current) return;
    setFloatingPos({
      x: e.clientX - dragOffset.current.x,
      y: e.clientY - dragOffset.current.y
    });
  }, []);

  const handleMouseUpDrag = useCallback(() => {
    isDragging.current = false;
    document.removeEventListener("mousemove", handleMouseMoveDrag);
    document.removeEventListener("mouseup", handleMouseUpDrag);
    document.body.style.userSelect = "";
  }, [handleMouseMoveDrag]);

  // --- HANDLERS: RESIZING ---
  const handleMouseDownResize = (e) => {
    if (docked) return;
    e.stopPropagation();
    isResizing.current = true;
    resizeStart.current = {
      x: e.clientX,
      y: e.clientY,
      w: floatingSize.w,
      h: floatingSize.h
    };

    document.addEventListener("mousemove", handleMouseMoveResize);
    document.addEventListener("mouseup", handleMouseUpResize);
    document.body.style.userSelect = "none";
  };

  const handleMouseMoveResize = useCallback((e) => {
    if (!isResizing.current) return;
    const deltaX = e.clientX - resizeStart.current.x;
    const deltaY = e.clientY - resizeStart.current.y;

    const newW = Math.max(600, resizeStart.current.w + deltaX);
    const newH = Math.max(400, resizeStart.current.h + deltaY);

    setFloatingSize({ w: newW, h: newH });
  }, []);

  const handleMouseUpResize = useCallback(() => {
    isResizing.current = false;
    document.removeEventListener("mousemove", handleMouseMoveResize);
    document.removeEventListener("mouseup", handleMouseUpResize);
    document.body.style.userSelect = "";
  }, [handleMouseMoveResize]);

  // --- ACTIONS ---
  const toggleDock = () => {
    setDocked(!docked);
  };

  const resetLayout = () => {
    if (!docked) {
      setFloatingPos({ x: 100, y: 100 });
      setFloatingSize({ w: 900, h: 600 });
    }
  };

  const refreshData = () => {
    if (isRefreshing) return;
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1200);
  };

  // --- RENDER HELPERS ---
  const containerStyle = docked
    ? {}
    : {
      position: "fixed",
      left: floatingPos.x,
      top: floatingPos.y,
      width: floatingSize.w,
      height: floatingSize.h,
      minWidth: "600px",
      minHeight: "400px",
      zIndex: 9999
    };

  return (
    <div
      className={`wallet-data-root ${docked ? "docked" : "floating"}`}
      ref={panelRef}
      style={containerStyle}
    >
      {/* HEADER / DRAG HANDLE */}
      <div
        className="wallet-data-header"
        ref={dragRef}
        onMouseDown={handleMouseDownDrag}
        title={!docked ? "Drag to move" : ""}
      >
        <div className="wd-header-left">
          <span className="wallet-section-title gold">WALLET DATA</span>
          <div className="wd-tabs">
            <button
              className={activeTab === "holdings" ? "active" : ""}
              onClick={() => setActiveTab("holdings")}
            >
              HOLDINGS
            </button>
            <button
              className={activeTab === "history" ? "active" : ""}
              onClick={() => setActiveTab("history")}
            >
              HISTORY
            </button>
          </div>
        </div>

        <div className="wd-header-right">
          <div className="wd-search-wrap">
            <input
              type="text"
              placeholder="Filter..."
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
            />
          </div>

          <button onClick={refreshData} disabled={isRefreshing} title="Refresh Data">
            {isRefreshing ? "⟳" : "↻"}
          </button>

          <button onClick={resetLayout} title="Reset Layout">
            ⊡
          </button>

          <button onClick={toggleDock} title={docked ? "Undock" : "Dock"}>
            {docked ? "↗" : "↙"}
          </button>

          {!docked && (
            <button className="close-btn" onClick={() => setDocked(true)} title="Minimize">
              ×
            </button>
          )}
        </div>
      </div>

      {/* CONTENT AREA */}
      <div className="wallet-data-content">
        {activeTab === "holdings" && (
          <WalletHoldings filter={filterText} isRefreshing={isRefreshing} />
        )}
        {activeTab === "history" && (
          <WalletHistory filter={filterText} isRefreshing={isRefreshing} />
        )}
      </div>

      {/* RESIZE HANDLE (Floating Only) */}
      {!docked && (
        <div className="wd-resize-handle" onMouseDown={handleMouseDownResize}>
          ◢
        </div>
      )}
    </div>
  );
}
