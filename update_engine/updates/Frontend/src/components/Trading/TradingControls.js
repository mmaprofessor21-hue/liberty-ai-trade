
// TIMESTAMP: PART G
import { SharedAITradingMapper } from "./SharedAITradingMapper";

export default function TradingControls(props) {
    const { externalAIState, onTradingStateChange } = props;

    const mapped = SharedAITradingMapper.mapAIStateToTrading(externalAIState || {});

    return (
        <div className="trading-controls">
            <p>Sniper Mode: {mapped.sniper ? "ON" : "OFF"}</p>
            <p>Risk Mode: {mapped.risk}</p>
            <p>Auto-Trade: {mapped.auto ? "ENABLED" : "DISABLED"}</p>
        </div>
    );
}
