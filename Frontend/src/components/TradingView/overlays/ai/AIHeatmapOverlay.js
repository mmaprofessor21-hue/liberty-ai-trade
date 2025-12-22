
import React, { useEffect, useRef } from "react";
import "./AIHeatmapOverlay.css";

/**
 * PART 6B — Heatmap Overlay
 */

export default function AIHeatmapOverlay({ heat }) {

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

        const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
        gradient.addColorStop(0, `rgba(255, 50, 50, ${0.25 * heat})`);
        gradient.addColorStop(1, `rgba(50, 255, 120, ${0.25 * (1 - heat)})`);

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

    }, [heat]);

    return <canvas ref={canvasRef} className="ai-heatmap-overlay"></canvas>;
}
