
// TIMESTAMP: 2025-12-08 13:11:21
import "./TradingSidebar.css";

export default function TradingSidebar() {
    return (
        <div className="trading-sidebar">
            <h3 className="sidebar-title">Trading Controls</h3>

            <div className="sidebar-section">
                <label>Symbol</label>
                <input type="text" placeholder="BTC/USD" />
            </div>

            <div className="sidebar-section">
                <label>Interval</label>
                <select>
                    <option>1m</option>
                    <option>5m</option>
                    <option>15m</option>
                    <option>1h</option>
                    <option>4h</option>
                    <option>1d</option>
                </select>
            </div>

            <div className="sidebar-section">
                <label>Sentiment Source</label>
                <select>
                    <option>Social</option>
                    <option>Orderflow</option>
                    <option>AI Blend</option>
                </select>
            </div>

            <div className="sidebar-section">
                <button className="apply-btn">Apply</button>
            </div>
        </div>
    );
}
