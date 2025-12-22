// DO NOT MODIFY OUTSIDE README_UPDATER RULES
/* TIMESTAMP: 2025-12-21_15-01-22 */

import React, { useEffect, useRef } from 'react';
import './KPIItem.css';

export default function KPIItem({ label, value, icon }) {

  const valueRef = useRef(null);

  useEffect(() => {
    if (!valueRef.current) return;

    const raw = parseFloat(String(value).replace(/[^0-9.]/g, ""));
    if (isNaN(raw)) {
      valueRef.current.textContent = value;
      return;
    }

    let current = 0;
    const duration = 900;
    const steps = 45;
    const increment = raw / steps;
    let frame = 0;

    const animation = setInterval(() => {
      frame++;
      current += increment;

      if (frame >= steps) {
        valueRef.current.textContent = value;
        clearInterval(animation);
      } else {
        valueRef.current.textContent = current.toFixed(2);
      }
    }, duration / steps);

    return () => clearInterval(animation);
  }, [value]);


  return (
    <div className="kpi-item fade-in">
      <div className="kpi-left">
        <span className="kpi-icon">{icon}</span>
        <span className="kpi-label">{label}</span>
      </div>

      <div className="kpi-value" ref={valueRef}>
        {value}
      </div>
    </div>
  );
}
