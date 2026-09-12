import { useState } from 'react';
import { GraduationCap, CheckCircle2 } from 'lucide-react';
import { LESSONS, CHECKLIST } from '../data/academy';

export function Academy() {
  const [done, setDone] = useState<string[]>([]);
  const [checks, setChecks] = useState<string[]>([]);
  const [filter, setFilter] = useState('All');
  const lessons = LESSONS.filter((l) => filter === 'All' || l.level === filter);
  const toggle = (list: string[], set: (v: string[]) => void, id: string) =>
    set(list.includes(id) ? list.filter((x) => x !== id) : [...list, id]);

  return (
    <div className="mx-auto max-w-6xl space-y-6 px-6 pb-16">
      <div className="glass rounded-2xl p-6">
        <h2 className="flex items-center gap-2 text-xl font-bold"><GraduationCap className="h-5 w-5 text-btc" /> Privacy Academy</h2>
        <p className="text-sm text-slate-400">Bite-size lessons + a score-improvement checklist. Progress: {done.length}/{LESSONS.length} lessons · {checks.length}/{CHECKLIST.length} habits</p>
        <div className="mt-3 flex gap-2">{['All', 'Beginner', 'Intermediate', 'Advanced'].map((f) => (
          <button key={f} onClick={() => setFilter(f)} className={`rounded-full px-4 py-1 text-xs ${filter === f ? 'bg-btc text-black font-semibold' : 'border border-white/10'}`}>{f}</button>
        ))}</div>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {lessons.map((l) => (
          <div key={l.id} className="glass rounded-2xl p-5 hover:border-btc/40">
            <div className="flex items-center justify-between"><span className="text-2xl">{l.icon}</span>
              <span className="rounded-full bg-white/5 px-2 py-0.5 text-[11px] text-slate-400">{l.level}</span></div>
            <h3 className="mt-2 font-semibold">{l.title}</h3><p className="mt-1 text-sm text-slate-400">{l.body}</p>
            <button onClick={() => toggle(done, setDone, l.id)} className="mt-3 flex items-center gap-1 text-xs text-cyber">
              <CheckCircle2 className={`h-4 w-4 ${done.includes(l.id) ? 'text-green-400' : ''}`} />
              {done.includes(l.id) ? 'Completed' : 'Mark complete'}</button>
          </div>
        ))}
      </div>
      <div className="glass rounded-2xl p-6">
        <h3 className="font-semibold text-btc">Privacy Score Improvement Checklist</h3>
        <div className="mt-3 grid gap-2 md:grid-cols-2">{CHECKLIST.map((c) => (
          <button key={c} onClick={() => toggle(checks, setChecks, c)} className="flex items-start gap-2 rounded-xl border border-white/5 bg-black/30 p-3 text-left text-sm">
            <CheckCircle2 className={`mt-0.5 h-4 w-4 shrink-0 ${checks.includes(c) ? 'text-green-400' : 'text-slate-600'}`} />{c}</button>
        ))}</div>
      </div>
    </div>
  );
}
