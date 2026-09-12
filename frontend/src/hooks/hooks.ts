import { useState } from 'react';
import { useEffect } from 'react';
import { api } from '../lib/api';

export function useBackendHealth() {
  const [online, setOnline] = useState<boolean | null>(null);
  useEffect(() => {
    api.health().then(() => setOnline(true)).catch(() => setOnline(false));
  }, []);
  return online;
}

export function useDemos() {
  const [demos, setDemos] = useState<any[]>([]);
  useEffect(() => { api.demos().then(setDemos).catch(() => setDemos([])); }, []);
  return demos;
}
