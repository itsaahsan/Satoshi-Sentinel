import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

export function ScoreRing({ score, size = 148 }: { score: number; size?: number }) {
  const [v, setV] = useState(0);
  useEffect(() => {
    const t0 = performance.now();
    const step = (t: number) => {
      const p = Math.min(1, (t - t0) / 900);
      setV(Math.round(score * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [score]);
  const color = score >= 70 ? '#22c55e' : score >= 45 ? '#f59e0b' : '#ef4444';
  const r = 60; const c = 2 * Math.PI * r;
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg viewBox="0 0 140 140" width={size} height={size}>
        <circle cx="70" cy="70" r={r} stroke="rgba(255,255,255,.08)" strokeWidth="12" fill="none" />
        <motion.circle cx="70" cy="70" r={r} stroke={color} strokeWidth="12" fill="none"
          strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c - (c * v) / 100}
          transform="rotate(-90 70 70)" />
      </svg>
      <div className="absolute inset-0 grid place-items-center">
        <div className="text-center">
          <div className="text-4xl font-bold" style={{ color }}>{v}</div>
          <div className="text-xs text-slate-400">/ 100 privacy</div>
        </div>
      </div>
    </div>
  );
}

export function Background() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10">
      <div className="absolute inset-0 grid-bg" />
      <div className="absolute -top-40 left-1/3 h-96 w-96 rounded-full bg-btc/15 blur-[120px]" />
      <div className="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-cyber/10 blur-[120px]" />
      <div className="absolute top-1/2 left-0 h-72 w-72 rounded-full bg-nostri/10 blur-[120px]" />
    </div>
  );
}

export function LevelBadge({ level }: { level: string }) {
  const map: Record<string, string> = {
    High: 'bg-red-500/15 text-red-300 border-red-500/30',
    Medium: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    Low: 'bg-green-500/15 text-green-300 border-green-500/30',
    high: 'bg-red-500/15 text-red-300 border-red-500/30',
    medium: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    low: 'bg-green-500/15 text-green-300 border-green-500/30',
  };
  return <span className={`rounded-full border px-2.5 py-0.5 text-xs font-semibold ${map[level] ?? map.Low}`}>{level}</span>;
}
