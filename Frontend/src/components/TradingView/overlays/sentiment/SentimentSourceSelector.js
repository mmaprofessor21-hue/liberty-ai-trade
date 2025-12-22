
import React from 'react';
import './SentimentSourceSelector.css';

export default function SentimentSourceSelector({ source, setSource }) {
    return (
        <div className="sentiment-source-wrapper">
            <label className="sentiment-source-label">Sentiment Source</label>
            <select
                className="sentiment-source-select"
                value={source}
                onChange={(e) => setSource(e.target.value)}
            >
                <option value="social">Social (X/Twitter)</option>
                <option value="news">News</option>
                <option value="reddit">Reddit</option>
                <option value="telegram">Telegram</option>
                <option value="fusion">AI Fusion Score</option>
            </select>
        </div>
    );
}
