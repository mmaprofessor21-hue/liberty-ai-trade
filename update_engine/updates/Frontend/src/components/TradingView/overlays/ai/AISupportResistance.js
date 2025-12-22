
import React, { useEffect, useRef } from "react";
import "./AISupportResistance.css";

/**
 * PART 6B — Support/Resistance Shading
 */

export default function AISupportResistance({ strength }) {

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

        const supportY = canvas.height * 0.75;
        const resistanceY = canvas.height * 0.25;

        ctx.fillStyle = `rgba(80, 255, 120, ${0.15 * strength})`;
        ctx.fillRect(0, supportY, canvas.width, canvas.height - supportY);

        ctx.fillStyle = `rgba(255, 80, 80, ${0.15 * strength})`;
        ctx.fillRect(0, 0, canvas.width, resistanceY);

    }, [strength]);

    return <canvas ref={canvasRef} className="ai-support-resistance"></canvas>;
}
