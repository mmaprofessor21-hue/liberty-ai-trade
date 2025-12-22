
import React, { useState } from "react";
import "./HoldingsPanel.css";

export default function HoldingsPanel() {

    const [holdings] = useState([
        { token: "SOL", amount: 24, value: 1650 },
        { token: "BTC", amount: 0.035, value: 3100 },
        { token: "XRP", amount: 900, value: 520 },
        { token: "BONK", amount: 120000, value: 160 },
        { token: "ETH", amount: 1.2, value: 4300 },
        { token: "ADA", amount: 4000, value: 120 },
        { token: "PEPE", amount: 8000000, value: 90 },
        { token: "DOGE", amount: 500, value: 45 }
    ]);

    return (
        <div className="holdings-panel">
            {holdings.map((row, idx) => (
                <div className="holding-row" key={idx}>
                    <span className="col-token">{row.token}</span>
                    <span className="col-amount">{row.amount}</span>
                    <span className="col-value">${row.value}</span>
                </div>
            ))}
        </div>
    );
}
