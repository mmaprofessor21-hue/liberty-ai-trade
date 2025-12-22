
import React, { useEffect, useRef } from "react";
import "./AITendencyCloud.css";

/**
 * PART 6B — Trend Cloud Overlay
 */

export default function AITendencyCloud({ trend }) {

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

        const gradient = ctx.createLinearGradient(0, canvas.height, canvas.width, 0);

        if (trend > 0) {
            gradient.addColorStop(0, "rgba(80, 255, 120, 0.18)");
            gradient.addColorStop(1, "rgba(20, 180, 90, 0.03)");
        } else {
            gradient.addColorStop(0, "rgba(255, 80, 80, 0.18)");
            gradient.addColorStop(1, "rgba(180, 40, 40, 0.03)");
        }

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

    }, [trend]);

    return <canvas ref={canvasRef} className="ai-tendency-cloud"></canvas>;
}
