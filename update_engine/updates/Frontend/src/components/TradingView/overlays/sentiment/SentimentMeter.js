
import React, { useEffect, useState } from "react";
import "./SentimentMeter.css";

export default function SentimentMeter({ score, token, source }) {

    const [color, setColor] = useState("#ff4d4d");

    useEffect(() => {
        if (score <= 20) setColor("#ff4d4d");
        else if (score <= 40) setColor("#ff884d");
        else if (score <= 60) setColor("#e2e24d");
        else if (score <= 80) setColor("#8cff7a");
        else setColor("#4dff88");
    }, [score]);

    return (
        <div className="sentiment-wrapper">
            <div className="sentiment-header-row">
                <div className="sentiment-label">
                    {token ? `${token} Sentiment` : "Sentiment"}
                </div>
                <div className="sentiment-source-tag">{source.toUpperCase()}</div>
            </div>

            <div className="sentiment-bar">
                <div 
                    className="sentiment-fill"
                    style={{ width: `${score}%`, background: color }}
                ></div>
            </div>

            <div className="sentiment-score">{score}%</div>
        </div>
    );
}
