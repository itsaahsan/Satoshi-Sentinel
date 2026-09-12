#!/usr/bin/env bash
# Satoshi Sentinel — one-command local demo (macOS/Linux).
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
(cd "$ROOT/backend" && python3 -m uvicorn app.main:app --reload) &
(cd "$ROOT/frontend" && npm run dev) &
wait
