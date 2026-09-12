"""Nostr: mock-friendly relay status + community feed + publish stub."""
from __future__ import annotations
import secrets, time
from ..config import settings

COMMUNITY_POSTS = [
    {"id": "note1a", "author": "npub1sentinel…privacy", "time": "2h ago",
     "content": "Privacy tip: generate a fresh Bitcoin address for every invoice. Reuse is the #1 beginner leak."},
    {"id": "note1b", "author": "npub1coinjoin…guide", "time": "5h ago",
     "content": "CoinJoin isn't magic — understand coordinators, fees, and post-mix spending before you try it."},
    {"id": "note1c", "author": "npub1lightning…fan", "time": "1d ago",
     "content": "Using Lightning for small recurring payments keeps your on-chain graph quiet. Good default."},
    {"id": "note1d", "author": "npub1utxo…nerd", "time": "2d ago",
     "content": "Learn coin control this week: open your wallet's UTXO list and label every coin's source."},
]


def generate_demo_identity() -> dict:
    rand = secrets.token_hex(16)
    return {"npub": f"npub1demo{rand[:12]}…sentinel", "note": "Demo identity only — never use with real funds."}


def relay_status() -> dict:
    return {"relay": settings.nostr_default_relay, "status": "reachable (demo)",
            "note": "Hackathon demo: relay treated as reachable; posts are local mock notes."}


def get_feed() -> list[dict]:
    return COMMUNITY_POSTS


def publish_note(content: str, author: str = "anonymous") -> dict:
    safe = (content or "")[:280]
    banned = ["seed", "private key", "nsec1"]
    lowered = safe.lower()
    if any(b in lowered for b in banned):
        return {"ok": False, "error": "Refused: never publish seeds or private keys to Nostr."}
    note = {"id": f"note{secrets.token_hex(4)}", "author": author, "time": "just now", "content": safe}
    COMMUNITY_POSTS.insert(0, note)
    return {"ok": True, "note": note, "relay": settings.nostr_default_relay}
