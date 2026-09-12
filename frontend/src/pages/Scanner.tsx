import { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader2, ScanSearch, TriangleAlert, BadgeCheck } from 'lucide-react';
import { api, ScanResult } from '../lib/api';
import { ScoreRing, LevelBadge } from '../components/ui';
import { TxGraph } from '../components/TxGraph';
import { useDemos } from '../hooks/hooks';

export function Scanner({ initial, onScan, result, setResult }: {
  initial: string; onScan: (r: ScanResult) => void; result: ScanResult | null; setResult: (r: ScanResult | null) => void;
}) {
  const [addr, setAddr] = useState(initial);
  const [mode, setMode] = useState('demo');
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const [expl, setExpl] = useState('');
  const demos = useDemos();

  const run = async (a?: string) => {
    const address = (a ?? addr).trim();
    if (!address) return;
    setLoading(true); setErr(''); setExpl('');
    try { const r = await api.scan(address, mode); setResult(r); onScan(r); }
    catch { setErr('Backend unreachable. Start it with: uvicorn app.main:app --reload (backend/).'); }
    finally { setLoading(false); }
  };

  return (
    <div className="mx-auto max-w-6xl space-y-6 px-6 pb-16">
      <div className="glass scanline relative overflow-hidden rounded-2xl p-6">
        <h2 className="flex items-center gap-2 text-xl font-bold"><ScanSearch className="h-5 w-5 text-cyber" /> Wallet Scanner</h2>
        <p className="mt-1 text-sm text-slate-400">Paste any Bitcoin address — analysis uses public data only. Try a demo wallet below.</p>
        <div className="mt-4 flex flex-col gap-3 md:flex-row">
          <input value={addr} onChange={(e) => setAddr(e.target.value)} placeholder="bc1q… or demo address"
            className="mono flex-1 rounded-xl border border-white/10 bg-black/40 px-4 py-3 text-sm outline-none focus:border-cyber/60" />
          <select value={mode} onChange={(e) => setMode(e.target.value)} className="rounded-xl border border-white/10 bg-black/40 px-3 py-3 text-sm">
            <option value="demo">Demo mode</option><option value="live">Live mode</option>
          </select>
          <button onClick={() => run()} disabled={loading} className="btn-btc flex items-center justify-center gap-2 rounded-xl px-6 py-3 disabled:opacity-50">
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : null} {loading ? 'Scanning public data…' : 'Analyze Privacy'}
          </button>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {(demos.length ? demos : [{ address: 'bc1qdemo-beginner-privacy-95', label: 'Beginner · 95' }, { address: 'bc1qdemo-active-privacy-54', label: 'Active · 54' }, { address: 'bc1qdemo-exposed-privacy-28', label: 'Exposed · 28' }]).map((d: any) => (
            <button key={d.address} onClick={() => { setAddr(d.address); run(d.address); }}
              className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs hover:border-btc/60">⚡ {d.label} <span className="mono text-slate-500">{d.address.slice(0, 18)}…</span></button>
          ))}
        </div>
        {loading && <div className="mono mt-4 text-xs text-cyber">▸ fetching transactions ▸ clustering ▸ scoring ▸ AI summary…</div>}
        {err && <p className="mt-3 text-sm text-red-300">{err}</p>}
      </div>

      {result && (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="glass flex items-center gap-5 rounded-2xl p-6 md:col-span-1">
              <ScoreRing score={result.score} />
              <div><LevelBadge level={result.risk_band} /><h3 className="mt-2 font-bold">{result.label}</h3>
                <p className="mono text-xs text-slate-500">{result.address}</p>
                <p className="mono mt-1 text-[11px] text-slate-500">source: {result.source} · mode: {result.mode}</p></div>
            </div>
            <div className="glass rounded-2xl p-6 md:col-span-2">
              <h4 className="font-semibold text-cyber">Sentinel summary</h4>
              <p className="mt-2 text-slate-200">{result.summary}</p>
              <div className="mt-3 space-y-1.5">
                {result.concerns.map((c, i) => <p key={i} className="flex gap-2 text-sm text-slate-300"><TriangleAlert className="h-4 w-4 shrink-0 text-amber-400" />{c}</p>)}
                {!result.concerns.length && <p className="flex gap-2 text-sm text-green-300"><BadgeCheck className="h-4 w-4" />No major concerns in this sample.</p>}
              </div>
            </div>
          </div>

          <div className="glass rounded-2xl p-6">
            <h4 className="font-semibold">Risk breakdown</h4>
            <div className="mt-3 overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="text-left text-slate-500"><th className="py-2">Risk category</th><th>Score</th><th>Level</th><th>Detail</th></tr></thead>
                <tbody>{Object.entries(result.categories).map(([k, c]: any) => (
                  <tr key={k} className="border-t border-white/5"><td className="py-2 font-medium capitalize">{k.replace('_', ' ')}</td>
                    <td className="mono">{c.score}</td><td><LevelBadge level={c.level} /></td><td className="max-w-md text-slate-400">{c.detail}</td></tr>
                ))}</tbody>
              </table>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="glass rounded-2xl p-6">
              <h4 className="font-semibold text-btc">Personalized recommendations</h4>
              <ul className="mt-3 space-y-3">{result.recommendations.map((r, i) => (
                <li key={i} className="rounded-xl border border-white/5 bg-black/30 p-3 text-sm">
                  <span className="font-semibold">{r.title}</span> <LevelBadge level={r.priority} />
                  <p className="mt-1 text-slate-400">{r.detail}</p></li>))}</ul>
            </div>
            <div className="glass rounded-2xl p-6">
              <h4 className="font-semibold">Recent transactions ({result.stats.tx_count})</h4>
              <ul className="mt-3 max-h-72 space-y-2 overflow-auto">
                {(result.transactions || []).map((t: any) => (
                  <li key={t.txid} className="mono rounded-lg border border-white/5 bg-black/30 p-2.5 text-xs">
                    <span className="text-cyber">{t.txid}</span> · {t.direction} · {t.amount_btc} BTC<br />
                    <span className="text-slate-500">{t.label} · {t.date}</span></li>))}
              </ul>
            </div>
          </div>

          <div>
            <h4 className="mb-2 font-semibold">Transaction graph <span className="text-xs font-normal text-slate-500">(click an edge for AI explanation)</span></h4>
            <TxGraph graph={result.graph} wallet={result.address} onSelect={(t) => setExpl(t.explanation)} />
            {expl && <div className="glass mt-3 rounded-2xl border-l-4 border-l-cyber p-4 text-sm">{expl}</div>}
          </div>
          <p className="mono text-xs text-slate-500">{result.disclaimer}</p>
        </motion.div>
      )}
    </div>
  );
}
