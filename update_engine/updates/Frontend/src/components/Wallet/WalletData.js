import React, { useState, useRef } from "react";
import "./WalletData.css";

export default function WalletData() {
  const [tab, setTab] = useState("holdings");
  const [docked, setDocked] = useState(true);
  const [pos, setPos] = useState({ x: 200, y: 200 });
  const [size, setSize] = useState({ w: 900, h: 360 });
  const dragRef = useRef(null);

  const holdings = [
    { token: "SOL", amount: "1.25", pl: "+42.10" },
    { token: "BONK", amount: "500k", pl: "-18.44" },
    { token: "WIF", amount: "220", pl: "+9.02" },
    { token: "JTO", amount: "14", pl: "+3.11" },
    { token: "RAY", amount: "8.4", pl: "-1.22" },
    { token: "PYTH", amount: "310", pl: "+6.90" },
    { token: "ORCA", amount: "19", pl: "+0.88" },
    { token: "EXTRA", amount: "99", pl: "+1.01" }
  ];

  const history = [
    { time: "10:22", token: "SOL", action: "BUY", amount: "1.25", pl: "+42.10" },
    { time: "10:21", token: "BONK", action: "SELL", amount: "500k", pl: "-18.44" },
    { time: "10:20", token: "WIF", action: "SELL", amount: "220", pl: "+9.02" },
    { time: "10:18", token: "JTO", action: "BUY", amount: "14", pl: "+3.11" },
    { time: "10:17", token: "RAY", action: "BUY", amount: "8.4", pl: "-1.22" },
    { time: "10:16", token: "PYTH", action: "SELL", amount: "310", pl: "+6.90" },
    { time: "10:15", token: "ORCA", action: "BUY", amount: "19", pl: "+0.88" },
    { time: "10:14", token: "TEST", action: "BUY", amount: "99", pl: "+1.01" }
  ];

  const data = tab === "holdings" ? holdings : history;
  const visible = docked ? data.slice(0, 7) : data;

  const onMouseDown = (e) => {
    if (docked) return;
    const startX = e.clientX - pos.x;
    const startY = e.clientY - pos.y;

    const move = (ev) => {
      setPos({ x: ev.clientX - startX, y: ev.clientY - startY });
    };

    const up = () => {
      document.removeEventListener("mousemove", move);
      document.removeEventListener("mouseup", up);
    };

    document.addEventListener("mousemove", move);
    document.addEventListener("mouseup", up);
  };

  return (
    <div
      className={`wallet-data-root ${docked ? "docked" : "floating"}`}
      style={!docked ? { left: pos.x, top: pos.y, width: size.w, height: size.h } : {}}
    >
      <div className="wallet-data-header" onMouseDown={onMouseDown} ref={dragRef}>
        <div className="wallet-data-tabs">
          <button onClick={() => setTab("holdings")} className={tab === "holdings" ? "active" : ""}>HOLDINGS</button>
          <button onClick={() => setTab("history")} className={tab === "history" ? "active" : ""}>HISTORY</button>
        </div>
      </div>

      <div className="wallet-data-table">
        <div className="wallet-data-row header">
          {tab === "holdings" ? (
            <>
              <span>TOKEN</span><span>AMOUNT</span><span>P/L</span>
            </>
          ) : (
            <>
              <span>TIME</span><span>TOKEN</span><span>ACTION</span><span>AMOUNT</span><span>P/L</span>
            </>
          )}
        </div>

        {visible.map((row, i) => (
          <div key={i} className="wallet-data-row">
            {tab === "holdings" ? (
              <>
                <span>{row.token}</span>
                <span>{row.amount}</span>
                <span>{row.pl}</span>
              </>
            ) : (
              <>
                <span>{row.time}</span>
                <span>{row.token}</span>
                <span>{row.action}</span>
                <span>{row.amount}</span>
                <span>{row.pl}</span>
              </>
            )}
          </div>
        ))}
      </div>

      <div className="wallet-data-footer">
        <button onClick={() => setDocked(!docked)}>
          {docked ? "UNDOCK TERMINAL" : "DOCK TERMINAL"}
        </button>
      </div>
    </div>
  );
}
