
import React from "react";
import "./AIExplanationPanel.css";

/**
 * PART 6A — Explainability Overlay
 */

export default function AIExplanationPanel({ token, explanation }) {
    if (!explanation) return null;

    return (
        <div className="ai-explain-panel">
            <div className="ai-explain-header">
                <span className="ai-explain-title">AI Analysis — {token}</span>
            </div>

            <div className="ai-explain-body">
                <div className="ai-explain-section">
                    <div className="ai-explain-label">Strategy:</div>
                    <div className="ai-explain-value">{explanation.strategy}</div>
                </div>

                <div className="ai-explain-section">
                    <div className="ai-explain-label">Confidence:</div>
                    <div className="ai-explain-value">
                        {explanation.strategyConf}%
                    </div>
                </div>

                <div className="ai-explain-section">
                    <div className="ai-explain-label">Sentiment:</div>
                    <div className="ai-explain-value">{explanation.sentiment}%</div>
                </div>

                <div className="ai-explain-section">
                    <div className="ai-explain-label">Reasoning:</div>
                    <div className="ai-explain-text">{explanation.summary}</div>
                </div>

                <div className="ai-explain-section">
                    <div className="ai-explain-label">Pattern:</div>
                    <div className="ai-explain-text">{explanation.pattern}</div>
                </div>
            </div>
        </div>
    );
}
