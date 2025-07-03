import React, { useRef, useEffect } from "react";

/**
 * Enhanced circular gauge for credit score (300-900)
 * - Gradient arc, animated, shadow, glow for high scores, modern look.
 */
const CreditScoreGauge = ({ score = 300, size = 160 }) => {
  const min = 300, max = 900;
  const percent = Math.max(0, Math.min(1, (score - min) / (max - min)));
  const angle = percent * 270; // 270deg arc
  const radius = size / 2 - 16;
  const cx = size / 2, cy = size / 2;
  const startAngle = 135, endAngle = 135 + angle;
  const polarToCartesian = (cx, cy, r, angle) => [
    cx + r * Math.cos((angle - 90) * Math.PI / 180),
    cy + r * Math.sin((angle - 90) * Math.PI / 180)
  ];
  const [sx, sy] = polarToCartesian(cx, cy, radius, startAngle);
  const [ex, ey] = polarToCartesian(cx, cy, radius, endAngle);
  const largeArc = angle > 180 ? 1 : 0;
  const pathData = `M ${sx} ${sy} A ${radius} ${radius} 0 ${largeArc} 1 ${ex} ${ey}`;
  // Color stops for gradient
  let gradId = "gauge-gradient-" + Math.round(score);
  let colorStops = [
    { stop: 0, color: "#22c55e" },    // green (low)
    { stop: 0.5, color: "#eab308" },  // yellow (mid)
    { stop: 0.75, color: "#f59e42" }, // orange (high-mid)
    { stop: 1, color: "#ef4444" },    // red (high)
  ];
  // Shadow for score
  const textShadow = score >= 750 ? "0 0 12px #22c55e55" : score >= 700 ? "0 0 8px #eab30866" : score >= 650 ? "0 0 6px #f59e4266" : "0 0 6px #ef444488";
  // Animate arc
  const arcRef = useRef(null);
  useEffect(() => {
    if (arcRef.current) {
      arcRef.current.style.strokeDasharray = arcRef.current.getTotalLength();
      arcRef.current.style.strokeDashoffset = arcRef.current.getTotalLength();
      setTimeout(() => {
        arcRef.current.style.transition = "stroke-dashoffset 1.2s cubic-bezier(.36,2,.53,.99)";
        arcRef.current.style.strokeDashoffset = 0;
      }, 100);
    }
  }, [score]);
  // Glow for high scores
  const glow = score >= 750 ? "drop-shadow(0 0 16px #22c55e88)" : score >= 700 ? "drop-shadow(0 0 12px #eab30866)" : "none";
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="mx-auto" style={{background: "radial-gradient(circle at 60% 40%, #f0fdfa 60%, #fff 100%)", borderRadius: "50%"}}>
      <defs>
        <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="0%">
          {colorStops.map((c, i) => (
            <stop key={i} offset={c.stop * 100 + "%"} stopColor={c.color} />
          ))}
        </linearGradient>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#888"/>
        </filter>
      </defs>
      {/* Track */}
      <path d={`M ${polarToCartesian(cx, cy, radius, 135).join(" ")} A ${radius} ${radius} 0 1 1 ${polarToCartesian(cx, cy, radius, 405).join(" ")}`} fill="none" stroke="#e5e7eb" strokeWidth="16" />
      {/* Progress - animated arc */}
      <path ref={arcRef} d={pathData} fill="none" stroke={`url(#${gradId})`} strokeWidth="16" strokeLinecap="round" filter="url(#shadow)" style={{filter: glow, strokeDasharray: 1000, strokeDashoffset: 1000}} />
      {/* Score circle */}
      
      <text x={cx} y={cy-4} textAnchor="middle" fontSize={size/7} fontWeight="bold" fill="#222" style={{filter: glow, textShadow}}>{score}</text>
      <text x={cx} y={cy+20} textAnchor="middle" fontSize={size/10} fill="#64748b">Credit Score</text>
    </svg>
  );
};

export default CreditScoreGauge;
