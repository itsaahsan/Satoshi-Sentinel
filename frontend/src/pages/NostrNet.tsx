import { useEffect, useState } from 'react';
import { Radio, KeyRound, Send, RefreshCw } from 'lucide-react';
import { api } from '../lib/api';

export function NostrNet() {
  const [status, setStatus] = useState<any>(null);
  const [posts, setPosts] = useState<any[]>([]);
  const [identity, setIdentity] = useState('');
  const [draft, setDraft] = useState('Privacy education alert: reusing one Bitcoin address links all your tips together. Use fresh addresses. #BitcoinPrivacy');
  const [msg, setMsg] = useState('');

  const load = async () => {
    try {
      const [s, f] = await Promise.all([api.nostrStatus(), api.nostrFeed()]);
      setStatus(s); setPosts(f.posts);
    } catch { setMsg('Backend unreachable — is FastAPI running?'); }
  };
  useEffect(() => { load(); }, []);

  const genId = async () => { try { const r = await api.nostrIdentity(); setIdentity(r.npub); } catch {} };
  const publish = async () => {
    setMsg('');
    try {
      const r = await api.nostrPublish(draft, identity || 'anonymous');
      if (r.ok) { setMsg('Published to community feed (demo relay).'); load(); }
      else setMsg(r.error);
    } catch { setMsg('Publish failed — backend unreachable.'); }
  };

  return (
    <div className="mx-auto max-w-5xl space-y-6 px-6 pb-16">
      <div className="glass rounded-2xl border-t-2 border-t-nostri p-6">
        <h2 className="flex items-center gap-2 text-xl font-bold"><Radio className="h-5 w-5 text-nostri" /> Nostr Network</h2>
        <p className="mt-1 text-sm text-slate-400">Censorship-resistant identity + educational privacy alerts. Never publish keys, seeds, or balances.</p>
        <div className="mt-4 grid gap-3 md:grid-cols-3">
          <div className="rounded-xl bg-black/30 p-4 text-sm"><p className="text-slate-500">Relay</p><p className="mono text-nostri">{status?.relay ?? '…'}</p><p className="text-green-300 text-xs">● {status?.status ?? 'connecting…'}</p></div>
          <div className="rounded-xl bg-black/30 p-4 text-sm"><p className="text-slate-500">Identity</p><p className="mono text-xs">{identity || 'not connected'}</p>
            <button onClick={genId} className="mt-2 flex items-center gap-1 rounded-lg border border-nostri/40 px-3 py-1.5 text-xs hover:bg-nostri/10"><KeyRound className="h-3 w-3" /> Generate demo identity</button></div>
          <div className="rounded-xl bg-black/30 p-4 text-sm"><p className="text-slate-500">Actions</p>
            <button onClick={load} className="mt-2 flex items-center gap-1 rounded-lg border border-white/10 px-3 py-1.5 text-xs hover:border-cyber/50"><RefreshCw className="h-3 w-3" /> Refresh feed</button></div>
        </div>
      </div>
      <div className="glass rounded-2xl p-6">
        <h3 className="font-semibold">Publish educational insight</h3>
        <textarea value={draft} onChange={(e) => setDraft(e.target.value)} rows={3} maxLength={280}
          className="mt-2 w-full rounded-xl border border-white/10 bg-black/40 p-3 text-sm outline-none focus:border-nostri/60" />
        <div className="mt-2 flex items-center justify-between">
          <span className="mono text-xs text-slate-500">{draft.length}/280</span>
          <button onClick={publish} className="flex items-center gap-2 rounded-xl bg-nostri px-5 py-2 text-sm font-semibold text-black hover:brightness-110"><Send className="h-4 w-4" /> Publish to Nostr</button>
        </div>
        {msg && <p className="mt-2 text-sm text-cyber">{msg}</p>}
      </div>
      <div className="space-y-3">
        {posts.map((p) => (
          <div key={p.id} className="glass rounded-2xl p-4"><p className="mono text-xs text-nostri">{p.author} · {p.time}</p><p className="mt-1 text-sm">{p.content}</p></div>
        ))}
      </div>
    </div>
  );
}
