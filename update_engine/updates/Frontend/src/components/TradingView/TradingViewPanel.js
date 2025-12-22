// 🚨 DO NOT MODIFY THIS FILE OUTSIDE THE RULES IN README_UPDATER.txt
// 🚫 NO IMPORT OVERRIDES | 🚫 NO PATH ASSUMPTIONS | ✅ ABSOLUTE STRUCTURE COMPLIANCE
/* TIMESTAMP PLACEHOLDER */

import React, { useState, useEffect } from "react";
import "./TradingViewPanel.css";

import TradingViewWidget from "./TradingViewWidget";
import TradingViewDock from "./TradingViewDock";
import TradingViewFloating from "./TradingViewFloating";
import TradingViewMarkers from "./TradingViewMarkers";

import SentimentMeter from "./SentimentMeter";
import SentimentSourceSelector from "./SentimentSourceSelector";
import SymbolDetector from "./SymbolDetector";
import TokenWatcher from "./TokenWatcher";
import TokenConfidence from "./TokenConfidence";
import StrategyIndicator from "./StrategyIndicator";

import { getActiveStrategy } from "./StrategyRouter";
import { routeAITrade } from "./AITradeRouter";
import { generateAIExplanation } from "./AIExplanationEngine";
import AIExplanationPanel from "./AIExplanationPanel";
import { startPredictionFeed } from "./PredictionFeed";

import AIControls from "../Controls/AI/AIControls";

export default function TradingViewPanel() {
    const [token, setToken] = useState("SOL");
    const [confidence, setConfidence] = useState(80);
    const [docked, setDocked] = useState(true);
    const [markers, setMarkers] = useState([]);
    const [source, setSource] = useState("social");
    const [sentiment, setSentiment] = useState(50);
    const [strategy, setStrategy] = useState("Neutral");
    const [strategyConf, setStrategyConf] = useState(50);
    const [explanation, setExplanation] = useState(null);

    const onResolve = (res) => {
        if (!res || !res.token) return;
        setToken(res.token);
        setConfidence(Math.min(res.score || 80, 100));
    };

    useEffect(() => {
        const result = getActiveStrategy(token, sentiment);
        setStrategy(result.strategy);
        setStrategyConf(result.confidence);

        setExplanation(
            generateAIExplanation(
                token,
                result.strategy,
                sentiment,
                result.confidence
            )
        );
    }, [token, sentiment]);

    useEffect(() => {
        setSentiment(Math.floor(Math.random() * 100));
    }, [token, source]);

    const addMarker = (payload) => {
        const routed = routeAITrade(
            payload.type,
            strategy,
            sentiment,
            token,
            strategyConf
        );

        setMarkers(prev => [...prev.slice(-90), {
            ...routed,
            x: payload.x,
            y: payload.y
        }]);
    };

    useEffect(() => {
        const stop = startPredictionFeed(
            addMarker,
            token,
            strategy,
            sentiment,
            strategyConf
        );
        return () => stop();
    }, [token, strategy, sentiment, strategyConf]);

    return (
        <div className="tv-panel-wrapper">

            <TradingViewDock docked={docked} setDocked={setDocked} />

            <SymbolDetector onResolve={onResolve} />
            <TokenWatcher onResolve={onResolve} />

            <AIExplanationPanel token={token} explanation={explanation} />
            <TokenConfidence token={token} confidence={confidence} />

            <SentimentSourceSelector source={source} setSource={setSource} />
            <SentimentMeter score={sentiment} token={token} source={source} />
            <StrategyIndicator strategy={strategy} confidence={strategyConf} />

            <AIControls
                onAIBuy={() => addMarker({ type: "buy", x: 0.9, y: 0.4 })}
                onAISell={() => addMarker({ type: "sell", x: 0.9, y: 0.6 })}
            />

            {docked && (
                <div className="tv-container docked">
                    <TradingViewWidget />
                    <TradingViewMarkers markers={markers} />
                </div>
            )}

            {!docked && (
                <TradingViewFloating>
                    <TradingViewWidget />
                    <TradingViewMarkers markers={markers} />
                </TradingViewFloating>
            )}
        </div>
    );
}
