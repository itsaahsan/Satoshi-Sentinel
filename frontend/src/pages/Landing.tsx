import { motion } from 'framer-motion';
import { Bitcoin, Radar, MessagesSquare, Network, GraduationCap, ArrowRight, ShieldCheck } from 'lucide-react';

export function Landing({ go }: { go: (v: string) => void }) {
  const cards = [
    { icon: <Radar className="h-5 w-5 text-cyber" />, t: 'AI Privacy Risk Scanner', d: 'Score any address 0–100 with transparent reuse, exposure & clustering signals.' },
    { icon: <MessagesSquare className="h-5 w-5 text-cyber" />, t: 'Sentinel AI Copilot', d: 'Beginner-clear answers on reuse, CoinJoin, UTXOs, surveillance & more.' },
    { icon: <Network className="h-5 w-5 text-nostri" />, t: 'Transaction Visualizer', d: 'Interactive graph with click-to-explain AI transaction summaries.' },
    { icon: <GraduationCap className="h-5 w-5 text-btc" />, t: 'Privacy Academy + Nostr', d: 'Learn privacy skills, then share tips over censorship-resistant Nostr.' },
  ];
  return (
    <div className="mx-auto max-w-6xl px-6 pb-20 pt-16">
      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} className="text-center">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-btc/15 ring-1 ring-btc/40">
          <Bitcoin className="h-9 w-9 text-btc" />
        </div>
        <p className="mono text-xs uppercase tracking-[0.3em] text-cyber">BOSS Battle Hackathon 2026 · Bitshala</p>
        <h1 className="mt-4 text-5xl font-bold leading-tight md:text-7xl">Satoshi <span className="text-btc">Sentinel</span></h1>
        <p className="mt-3 text-xl text-slate-300">Your AI Guardian for Bitcoin Privacy.</p>
        <p className="mx-auto mt-4 max-w-2xl text-slate-400">Understand your on-chain footprint. Discover privacy risks. Learn how to protect your financial freedom.</p>
        <div className="mt-8 flex justify-center gap-3">
          <button onClick={() => go('scan')} className="btn-btc flex items-center gap-2 rounded-xl px-6 py-3">Scan a Wallet <ArrowRight className="h-4 w-4" /></button>
          <button onClick={() => go('scan')} className="glass rounded-xl px-6 py-3 hover:border-cyber/50">Explore Demo</button>
        </div>
        <p className="mono mt-4 text-xs text-slate-500">DEMO MODE · works without API keys · no seeds · no keys · read-only</p>
      </motion.div>
      <div className="mt-14 grid gap-4 md:grid-cols-4">
        {cards.map((c, i) => (
          <motion.div key={c.t} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 + i * 0.08 }}
            className="glass rounded-2xl p-5 hover:border-cyber/40">
            {c.icon}<h3 className="mt-3 font-semibold">{c.t}</h3><p className="mt-1 text-sm text-slate-400">{c.d}</p>
          </motion.div>
        ))}
      </div>
      <div className="glass mt-8 flex items-start gap-3 rounded-2xl p-5">
        <ShieldCheck className="mt-0.5 h-5 w-5 shrink-0 text-green-400" />
        <p className="text-sm text-slate-300"><b>Privacy promise:</b> Satoshi Sentinel is an educational privacy analysis tool. It does not identify wallet owners, never asks for seed phrases or private keys, never moves funds, and does not provide financial or legal advice.</p>
      </div>
    </div>
  );
}
