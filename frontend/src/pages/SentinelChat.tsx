import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, Loader2 } from 'lucide-react';
import { api, ScanResult } from '../lib/api';

const SUGGESTED = [
  'Why is address reuse a privacy problem?',
  'How does Bitcoin surveillance work?',
  'What is CoinJoin?',
  'Explain UTXOs simply.',
  'What is my biggest privacy risk?',
  'What is Nostr?',
];

export function SentinelChat({ scan }: { scan: ScanResult | null }) {
  const [msgs, setMsgs] = useState<{ role: string; text: string }[]>([
    { role: 'ai', text: 'I’m **Sentinel AI**, your Bitcoin privacy tutor. Ask me anything — or try a suggested question below. I explain public data responsibly and never identify owners.' },
  ]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);

  const ask = async (q?: string) => {
    const question = (q ?? input).trim();
    if (!question || busy) return;
    setInput('');
    setMsgs((m) => [...m, { role: 'user', text: question }]);
    setBusy(true);
    const ctx = scan ? `Wallet ${scan.address}: score ${scan.score}/100 (${scan.risk_band} risk). Concerns: ${scan.concerns.join(' | ')}` : '';
    try {
      const r = await api.chat(question, ctx);
      setMsgs((m) => [...m, { role: 'ai', text: r.answer }]);
    } catch {
      setMsgs((m) => [...m, { role: 'ai', text: 'Backend unreachable — start it with `uvicorn app.main:app --reload` in backend/.' }]);
    } finally { setBusy(false); }
  };

  return (
    <div className="mx-auto max-w-3xl px-6 pb-16">
      <div className="glass rounded-2xl p-5 text-center">
        <Bot className="mx-auto h-8 w-8 text-cyber" />
        <h2 className="mt-1 text-xl font-bold">Sentinel AI</h2>
        <p className="text-sm text-slate-400">Bitcoin Privacy Intelligence {scan && <span className="mono text-btc">· context: {scan.label} ({scan.score}/100)</span>}</p>
      </div>
      <div className="mt-4 space-y-3">
        {msgs.map((m, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
            className={`rounded-2xl p-4 text-sm leading-relaxed ${m.role === 'ai' ? 'glass border-l-4 border-l-cyber' : 'ml-12 bg-btc/15 border border-btc/30'}`}>
            <p className="whitespace-pre-wrap">{m.text}</p>
          </motion.div>
        ))}
        {busy && <p className="mono flex items-center gap-2 text-xs text-cyber"><Loader2 className="h-3 w-3 animate-spin" /> sentinel is reasoning…</p>}
      </div>
      <div className="mt-3 flex flex-wrap gap-2">
        {SUGGESTED.map((s) => <button key={s} onClick={() => ask(s)} className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs hover:border-cyber/60">{s}</button>)}
      </div>
      <div className="mt-3 flex gap-2">
        <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && ask()}
          placeholder="Ask about Bitcoin privacy…" className="flex-1 rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm outline-none focus:border-cyber/60" />
        <button onClick={() => ask()} disabled={busy} className="btn-btc rounded-xl px-5"><Send className="h-4 w-4" /></button>
      </div>
    </div>
  );
}
