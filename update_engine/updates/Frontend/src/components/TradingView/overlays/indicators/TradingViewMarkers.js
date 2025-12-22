
import React, { useEffect, useRef } from "react";
import "./TradingViewMarkers.css";

/**
 * PART 5C — Marker Rendering Supports:
 *  - AI trade signals
 *  - Strategy-driven styles
 *  - Adaptive glow
 */

export default function TradingViewMarkers({ markers }) {

    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        const resize = () => {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
        };
        resize();

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        markers.forEach(m => {
            const x = m.x * canvas.width;
            const y = (1 - m.y) * canvas.height;

            ctx.beginPath();
            ctx.arc(x, y, m.style.size + 4, 0, Math.PI * 2);
            ctx.fillStyle = m.style.glow;
            ctx.fill();

            ctx.beginPath();
            ctx.arc(x, y, m.style.size, 0, Math.PI * 2);
            ctx.fillStyle = m.style.color;
            ctx.fill();

            ctx.font = "bold 12px Arial";
            ctx.fillStyle = "#111";
            ctx.textAlign = "center";
            ctx.fillText(m.type === "buy" ? "B" : "S", x, y + 4);
        });

    }, [markers]);


    return <canvas ref={canvasRef} className="tv-marker-canvas"></canvas>;
}
