
import React, { useState } from "react";
import "./TelegramControls.css";
import { FaPaperPlane, FaPlug, FaUnlink } from "react-icons/fa";

export default function TelegramControls() {

    const [connected, setConnected] = useState(false);
    const [msg, setMsg] = useState("");

    const connect = () => {
        setConnected(true);
        console.log("Telegram connected.");
    };

    const disconnect = () => {
        setConnected(false);
    };

    const sendMessage = () => {
        console.log("Send Telegram:", msg);
        setMsg("");
    };

    return (
        <div className="telegram-controls">

            <div className="tg-row">
                <FaPlug className="tg-icon" />
                <button 
                    className="tg-btn connect"
                    onClick={connect}
                    disabled={connected}
                >
                    Connect
                </button>

                <FaUnlink className="tg-icon" />
                <button 
                    className="tg-btn disconnect"
                    onClick={disconnect}
                    disabled={!connected}
                >
                    Disconnect
                </button>
            </div>

            <div className="tg-row">
                <input
                    className="tg-input"
                    placeholder="Send test message..."
                    value={msg}
                    onChange={(e) => setMsg(e.target.value)}
                />

                <button 
                    className="tg-btn send"
                    onClick={sendMessage}
                    disabled={!connected}
                >
                    <FaPaperPlane className="tg-icon" /> Send
                </button>
            </div>

        </div>
    );
}
