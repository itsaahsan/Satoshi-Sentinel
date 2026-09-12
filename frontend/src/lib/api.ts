const BASE = ((import.meta.env.VITE_API_URL as string | undefined) ?? '').replace(/\/$/, '');

async function req(path: string, opts: RequestInit = {}) {
  const r = await fetch(BASE + path, {
    ...opts,
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
  });
  if (!r.ok) throw new Error(`API ${r.status} on ${path}`);
  return r.json();
}

export const api = {
  scan: (address: string, mode = 'demo') =>
    req('/api/scan', { method: 'POST', body: JSON.stringify({ address, mode }) }),
  demos: () => req('/api/scan/demos'),
  chat: (message: string, context = '') =>
    req('/api/chat', { method: 'POST', body: JSON.stringify({ message, context }) }),
  explain: (tx: any, wallet_address = '') =>
    req('/api/explain', { method: 'POST', body: JSON.stringify({ tx, wallet_address }) }),
  nostrStatus: () => req('/api/nostr/status'),
  nostrFeed: () => req('/api/nostr/feed'),
  nostrIdentity: () => req('/api/nostr/identity'),
  nostrPublish: (content: string, author = 'anonymous') =>
    req('/api/nostr/publish', { method: 'POST', body: JSON.stringify({ content, author }) }),
  health: () => req('/api/health'),
};

export type ScanResult = {
  address: string; mode: string; source: string; label: string;
  score: number; risk_band: string; summary: string;
  categories: Record<string, { score: number; level: string; detail: string }>;
  concerns: string[]; recommendations: { title: string; priority: string; detail: string }[];
  transactions: any[]; graph: { nodes: any[]; edges: any[] };
  stats: Record<string, number>; disclaimer: string;
};
