
import React from "react";
import "./StrategyIndicator.css";

/**
 * Displays currently active AI strategy and confidence.
 */

export default function StrategyIndicator({ strategy, confidence }) {
    return (
        <div className="strategy-indicator-box">
            <div className="strategy-title">AI Strategy:</div>
            <div className="strategy-name">{strategy}</div>
            <div className="strategy-confidence">
                Confidence: {confidence}%
            </div>
        </div>
    );
}
