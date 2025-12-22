
import React, { useState } from "react";
import "./HistoryPanel.css";

export default function HistoryPanel() {

    const [logs] = useState([
        { time: "10:22", pair: "SOL/USDT", action: "BUY", amount: 200 },
        { time: "10:34", pair: "SOL/USDT", action: "SELL", amount: 215 },
        { time: "11:12", pair: "XRP/USDT", action: "BUY", amount: 0.54 },
        { time: "11:35", pair: "XRP/USDT", action: "SELL", amount: 0.60 },
        { time: "12:08", pair: "BTC/USDT", action: "BUY", amount: 31000 },
        { time: "12:25", pair: "BTC/USDT", action: "SELL", amount: 31400 },
        { time: "13:02", pair: "BONK/USDT", action: "BUY", amount: 0.000013 },
        { time: "13:48", pair: "BONK/USDT", action: "SELL", amount: 0.000016 }
    ]);

    return (
        <div className="history-panel">
            {logs.map((row, idx) => (
                <div className="history-row" key={idx}>
                    <span className="col-time">{row.time}</span>
                    <span className="col-pair">{row.pair}</span>
                    <span className={`col-action ${row.action.toLowerCase()}`}>
                        {row.action}
                    </span>
                    <span className="col-amt">{row.amount}</span>
                </div>
            ))}
        </div>
    );
}
