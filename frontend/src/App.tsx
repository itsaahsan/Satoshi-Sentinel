import { useState } from 'react';
import { Bitcoin, Radar, MessagesSquare, Network, GraduationCap, Home, Wifi, WifiOff } from 'lucide-react';
import { Background } from './components/ui';
import { Landing } from './pages/Landing';
import { Scanner } from './pages/Scanner';
import { SentinelChat } from './pages/SentinelChat';
import { NostrNet } from './pages/NostrNet';
import { Academy } from './pages/Academy';
import { useBackendHealth } from './hooks/hooks';
import type { ScanResult } from './lib/api';

const NAV = [
  { id: 'home', label: 'Overview', icon: Home },
  { id: 'scan', label: 'Wallet Scanner', icon: Radar },
  { id: 'chat', label: 'Sentinel AI', icon: MessagesSquare },
  { id: 'nostr', label: 'Nostr Network', icon: Network },
  { id: 'academy', label: 'Privacy Academy', icon: GraduationCap },
];

export default function App() {
  const [view, setView] = useState('home');
  const [scan, setScan] = useState<ScanResult | null>(null);
  const [addr] = useState('bc1qdemo-exposed-privacy-28');
  const online = useBackendHealth();

  const goScan = (r: ScanResult) => { setScan(r); };

  return (
    <div className="min-h-screen">
      <Background />
      <header className="sticky top-0 z-20 border-b border-white/10 bg-void/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <button onClick={() => setView('home')} className="flex items-center gap-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-btc/15 ring-1 ring-btc/40"><Bitcoin className="h-5 w-5 text-btc" /></span>
            <span className="font-bold">Satoshi <span className="text-btc">Sentinel</span></span>
          </button>
          <div className="mono flex items-center gap-3 text-[11px]">
            <span className={`flex items-center gap-1 ${online ? 'text-green-400' : online === false ? 'text-red-400' : 'text-slate-500'}`}>
              {online ? <Wifi className="h-3 w-3" /> : <WifiOff className="h-3 w-3" />} {online ? 'API online' : online === false ? 'API offline' : '…'}
            </span>
            <span className="rounded-full border border-cyber/40 px-2 py-0.5 text-cyber">DEMO</span>
          </div>
        </div>
      </header>

      {view === 'home' ? (
        <Landing go={(v) => setView(v)} />
      ) : (
        <div className="mx-auto flex max-w-7xl gap-6 px-0 py-6 md:px-6">
          <aside className="sticky top-[65px] hidden h-fit w-52 shrink-0 space-y-1 md:block">
            {NAV.map((n) => (
              <button key={n.id} onClick={() => setView(n.id)}
                className={`flex w-full items-center gap-2.5 rounded-xl px-4 py-2.5 text-sm ${view === n.id ? 'bg-white/10 text-white ring-1 ring-white/15' : 'text-slate-400 hover:bg-white/5'}`}>
                <n.icon className="h-4 w-4" /> {n.label}
              </button>
            ))}
            <div className="mono mt-4 rounded-xl border border-white/10 p-3 text-[11px] text-slate-500">
              Educational tool.<br />No keys. No seeds.<br />No fund movement.
            </div>
          </aside>
          <main className="min-w-0 flex-1">
            <div className="mb-4 flex gap-2 overflow-x-auto px-6 md:hidden">
              {NAV.map((n) => (
                <button key={n.id} onClick={() => setView(n.id)}
                  className={`whitespace-nowrap rounded-full px-4 py-1.5 text-xs ${view === n.id ? 'bg-btc text-black font-semibold' : 'border border-white/10'}`}>{n.label}</button>
              ))}
            </div>
            {view === 'scan' && <Scanner initial={addr} onScan={goScan} result={scan} setResult={setScan} />}
            {view === 'chat' && <SentinelChat scan={scan} />}
            {view === 'nostr' && <NostrNet />}
            {view === 'academy' && <Academy />}
          </main>
        </div>
      )}
      <footer className="mono border-t border-white/10 py-6 text-center text-[11px] text-slate-500">
        Satoshi Sentinel · BOSS Battle Hackathon 2026 · Educational privacy analysis — not financial/legal advice.
      </footer>
    </div>
  );
}
