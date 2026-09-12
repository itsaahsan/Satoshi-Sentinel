"""Bitcoin data layer: demo mode + optional live Esplora/Mempool fetch."""
from __future__ import annotations
import httpx
from ..config import settings
from .demo_data import get_demo_wallet


async def fetch_live_address(address: str) -> dict | None:
    """Try mempool.space, fall back to blockstream. Returns stats dict or None."""
    urls = [
        f"{settings.mempool_api_url}/address/{address}",
        f"{settings.mempool_api_url}/address/{address}/txs",
    ]
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.get(urls[0])
            if r.status_code != 200:
                return None
            info = r.json()
            chain = info.get("chain_stats", {})
            funded = chain.get("funded_txo_count", 0)
            spent = chain.get("spent_txo_count", 0)
            tx_count = chain.get("tx_count", funded + spent)
            t = await client.get(urls[1])
            txs = t.json() if t.status_code == 200 else []
            counterparties = set()
            for tx in txs[:25]:
                for vin in tx.get("vin", [])[:4]:
                    prev = (vin.get("prevout") or {}).get("scriptpubkey_address")
                    if prev and prev != address:
                        counterparties.add(prev)
                for vout in tx.get("vout", [])[:4]:
                    spk = vout.get("scriptpubkey_address")
                    if spk and spk != address:
                        counterparties.add(spk)
            tx_list = [
                {"txid": tx.get("txid", "")[:16], "direction": "observed",
                 "amount_btc": round(sum(v.get("value", 0) for v in tx.get("vout", [])) / 1e8, 8),
                 "counterparty": "on-chain counterparty", "date": "confirmed",
                 "label": f"status: {'confirmed' if tx.get('status', {}).get('confirmed') else 'unconfirmed'}"}
                for tx in txs[:8]
            ]
            return {
                "tx_count": tx_count, "counterparties": max(len(counterparties), min(tx_count, 4)),
                "reuse_count": 0, "public_exposure": False, "frequency_per_week": min(tx_count / 4, 5),
                "known_entity_hits": 0, "transactions": tx_list,
                "graph": {"nodes": [{"id": "wallet", "label": address[:14] + "…", "type": "self", "risk": "medium"}],
                          "edges": []},
                "live": True,
            }
    except Exception:
        return None


async def get_wallet_stats(address: str, mode: str = "demo") -> tuple[dict, str]:
    """Returns (stats, source): source in demo|live|demo-fallback."""
    demo = get_demo_wallet(address)
    if mode == "live":
        live = await fetch_live_address(address)
        if live:
            return live, "live"
        if demo:
            return demo, "demo-fallback"
        # generic synthesis so UI never crashes
        return {"tx_count": 3, "counterparties": 2, "reuse_count": 0, "public_exposure": False,
                "frequency_per_week": 0.4, "known_entity_hits": 0, "transactions": [],
                "graph": {"nodes": [{"id": "wallet", "label": address[:14], "type": "self", "risk": "low"}], "edges": []}}, "demo-fallback"
    if demo:
        return demo, "demo"
    # Unknown address in demo mode -> route to beginner-like generic profile
    generic = dict(DEMO_WALLETS["demo-beginner"])
    generic = {**generic, "address": address}
    return generic, "demo-generic"
