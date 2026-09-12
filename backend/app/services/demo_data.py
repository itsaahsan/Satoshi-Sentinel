"""Deterministic demo wallets: low / medium / high privacy risk. NEVER real owners."""
from __future__ import annotations

DEMO_WALLETS: dict[str, dict] = {
    "demo-beginner": {
        "label": "Beginner Wallet",
        "address": "bc1qdemo-beginner-privacy-95",
        "expected_score": 95,
        "summary": "Few transactions, no significant address reuse, limited public exposure.",
        "tx_count": 4,
        "counterparties": 3,
        "reuse_count": 0,
        "public_exposure": False,
        "frequency_per_week": 0.5,
        "known_entity_hits": 0,
        "transactions": [
            {"txid": "demo-beg-tx1", "direction": "received", "amount_btc": 0.012, "counterparty": "bc1q...swan", "date": "2026-06-02", "label": "First savings deposit"},
            {"txid": "demo-beg-tx2", "direction": "received", "amount_btc": 0.008, "counterparty": "bc1q...strike", "date": "2026-07-11", "label": "DCA buy withdrawal"},
            {"txid": "demo-beg-tx3", "direction": "sent", "amount_btc": 0.003, "counterparty": "bc1q...cold", "date": "2026-08-05", "label": "Move to cold storage"},
            {"txid": "demo-beg-tx4", "direction": "received", "amount_btc": 0.005, "counterparty": "bc1q...river", "date": "2026-08-28", "label": "DCA buy withdrawal"},
        ],
        "graph": {
            "nodes": [
                {"id": "wallet", "label": "Your wallet", "type": "self", "risk": "low"},
                {"id": "cp1", "label": "Exchange A", "type": "exchange", "risk": "low"},
                {"id": "cp2", "label": "Exchange B", "type": "exchange", "risk": "low"},
                {"id": "cp3", "label": "Cold storage", "type": "self", "risk": "low"},
            ],
            "edges": [
                {"id": "e1", "source": "cp1", "target": "wallet", "amount_btc": 0.012, "txid": "demo-beg-tx1"},
                {"id": "e2", "source": "cp2", "target": "wallet", "amount_btc": 0.008, "txid": "demo-beg-tx2"},
                {"id": "e3", "source": "wallet", "target": "cp3", "amount_btc": 0.003, "txid": "demo-beg-tx3"},
                {"id": "e4", "source": "cp1", "target": "wallet", "amount_btc": 0.005, "txid": "demo-beg-tx4"},
            ],
        },
    },
    "demo-active": {
        "label": "Active Wallet",
        "address": "bc1qdemo-active-privacy-54",
        "expected_score": 54,
        "summary": "Multiple transactions, some repeated interactions, moderate exposure.",
        "tx_count": 14,
        "counterparties": 8,
        "reuse_count": 5,
        "public_exposure": True,
        "frequency_per_week": 3.2,
        "known_entity_hits": 2,
        "transactions": [
            {"txid": "demo-act-tx1", "direction": "received", "amount_btc": 0.02, "counterparty": "bc1q...exchange", "date": "2026-04-01", "label": "Salary withdrawal"},
            {"txid": "demo-act-tx2", "direction": "sent", "amount_btc": 0.004, "counterparty": "bc1q...merchant", "date": "2026-04-09", "label": "Merchant payment (reused addr)"},
            {"txid": "demo-act-tx3", "direction": "sent", "amount_btc": 0.004, "counterparty": "bc1q...merchant", "date": "2026-04-23", "label": "Repeat merchant (reuse!)"},
            {"txid": "demo-act-tx4", "direction": "received", "amount_btc": 0.01, "counterparty": "bc1q...friend", "date": "2026-05-14", "label": "P2P receive"},
            {"txid": "demo-act-tx5", "direction": "sent", "amount_btc": 0.006, "counterparty": "bc1q...donation", "date": "2026-06-02", "label": "Public donation (posted on X)"},
        ],
        "graph": {
            "nodes": [
                {"id": "wallet", "label": "Your wallet", "type": "self", "risk": "medium"},
                {"id": "ex", "label": "Exchange", "type": "exchange", "risk": "low"},
                {"id": "merch", "label": "Merchant (reused)", "type": "merchant", "risk": "high"},
                {"id": "friend", "label": "P2P peer", "type": "peer", "risk": "medium"},
                {"id": "public", "label": "Public donation page", "type": "public", "risk": "high"},
                {"id": "c1", "label": "Counterparty cluster", "type": "unknown", "risk": "medium"},
            ],
            "edges": [
                {"id": "e1", "source": "ex", "target": "wallet", "amount_btc": 0.02, "txid": "demo-act-tx1"},
                {"id": "e2", "source": "wallet", "target": "merch", "amount_btc": 0.004, "txid": "demo-act-tx2"},
                {"id": "e3", "source": "wallet", "target": "merch", "amount_btc": 0.004, "txid": "demo-act-tx3"},
                {"id": "e4", "source": "friend", "target": "wallet", "amount_btc": 0.01, "txid": "demo-act-tx4"},
                {"id": "e5", "source": "wallet", "target": "public", "amount_btc": 0.006, "txid": "demo-act-tx5"},
                {"id": "e6", "source": "wallet", "target": "c1", "amount_btc": 0.002, "txid": "demo-act-tx6"},
            ],
        },
    },
    "demo-exposed": {
        "label": "Publicly Exposed Wallet",
        "address": "bc1qdemo-exposed-privacy-28",
        "expected_score": 28,
        "summary": "Frequent address reuse, many public interactions, high linking potential.",
        "tx_count": 47,
        "counterparties": 22,
        "reuse_count": 21,
        "public_exposure": True,
        "frequency_per_week": 9.8,
        "known_entity_hits": 7,
        "transactions": [
            {"txid": "demo-exp-tx1", "direction": "received", "amount_btc": 0.05, "counterparty": "bc1q...exchange", "date": "2026-01-05", "label": "Posted on donation page"},
            {"txid": "demo-exp-tx2", "direction": "received", "amount_btc": 0.002, "counterparty": "bc1q...fan1", "date": "2026-01-19", "label": "Tip (same reused address)"},
            {"txid": "demo-exp-tx3", "direction": "received", "amount_btc": 0.001, "counterparty": "bc1q...fan2", "date": "2026-02-02", "label": "Tip (same reused address)"},
            {"txid": "demo-exp-tx4", "direction": "sent", "amount_btc": 0.03, "counterparty": "bc1q...exchange", "date": "2026-03-04", "label": "Consolidation (links all inputs)"},
            {"txid": "demo-exp-tx5", "direction": "sent", "amount_btc": 0.005, "counterparty": "bc1q...vendor", "date": "2026-05-20", "label": "Vendor payment reveals balance"},
        ],
        "graph": {
            "nodes": [
                {"id": "wallet", "label": "Reused address", "type": "self", "risk": "high"},
                {"id": "fans", "label": "12 tippers", "type": "peer", "risk": "high"},
                {"id": "ex", "label": "Exchange", "type": "exchange", "risk": "medium"},
                {"id": "vendor", "label": "Vendor", "type": "merchant", "risk": "high"},
                {"id": "donors", "label": "Public donors", "type": "public", "risk": "high"},
                {"id": "cluster", "label": "Linked cluster (9 addrs)", "type": "unknown", "risk": "high"},
                {"id": "observer", "label": "Chain observer", "type": "public", "risk": "high"},
            ],
            "edges": [
                {"id": "e1", "source": "ex", "target": "wallet", "amount_btc": 0.05, "txid": "demo-exp-tx1"},
                {"id": "e2", "source": "fans", "target": "wallet", "amount_btc": 0.002, "txid": "demo-exp-tx2"},
                {"id": "e3", "source": "donors", "target": "wallet", "amount_btc": 0.001, "txid": "demo-exp-tx3"},
                {"id": "e4", "source": "wallet", "target": "ex", "amount_btc": 0.03, "txid": "demo-exp-tx4"},
                {"id": "e5", "source": "wallet", "target": "vendor", "amount_btc": 0.005, "txid": "demo-exp-tx5"},
                {"id": "e6", "source": "wallet", "target": "cluster", "amount_btc": 0.01, "txid": "demo-exp-tx6"},
                {"id": "e7", "source": "cluster", "target": "observer", "amount_btc": 0.0, "txid": "observed"},
            ],
        },
    },
}

DEMO_ADDRESS_INDEX = {w["address"]: key for key, w in DEMO_WALLETS.items()}


def get_demo_wallet(address: str) -> dict | None:
    address = (address or "").strip()
    if address in DEMO_WALLETS:
        return DEMO_WALLETS[address]
    if address in DEMO_ADDRESS_INDEX:
        return DEMO_WALLETS[DEMO_ADDRESS_INDEX[address]]
    lowered = address.lower()
    # Heuristic routing so any typed address lands on an interesting demo
    if "exposed" in lowered or "public" in lowered or "donat" in lowered:
        return DEMO_WALLETS["demo-exposed"]
    if "active" in lowered or "medium" in lowered:
        return DEMO_WALLETS["demo-active"]
    if lowered.startswith("bc1qdemo"):
        return DEMO_WALLETS["demo-beginner"]
    return None
