import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.services.privacy_engine import analyze_wallet, score_address_reuse
from app.services.demo_data import DEMO_WALLETS, get_demo_wallet
from app.services.ai_service import local_answer
from app.services import nostr_service

client = TestClient(app)


def test_reuse_detection_none():
    r = score_address_reuse(0, 5)
    assert r["score"] == 100 and r["level"] == "Low"


def test_reuse_detection_high():
    r = score_address_reuse(31, 47)
    assert r["level"] == "High" and r["score"] < 50


def test_privacy_score_ordering():
    scores = {k: analyze_wallet(v)["overall_score"] for k, v in DEMO_WALLETS.items()}
    assert scores["demo-beginner"] > scores["demo-active"] > scores["demo-exposed"]
    assert 70 <= scores["demo-beginner"] <= 95
    assert 20 <= scores["demo-exposed"] <= 40


def test_demo_wallets_load():
    assert len(DEMO_WALLETS) == 3
    assert get_demo_wallet("bc1qdemo-exposed-privacy-28")["expected_score"] == 28
    assert get_demo_wallet("anything-with-exposed-inside")["label"] == "Publicly Exposed Wallet"


def test_scan_endpoint_demo():
    r = client.post("/api/scan", json={"address": "bc1qdemo-active-privacy-54", "mode": "demo"})
    assert r.status_code == 200
    body = r.json()
    assert "score" in body and "recommendations" in body and "graph" in body
    assert body["disclaimer"]


def test_scan_demos_endpoint():
    assert client.get("/api/scan/demos").status_code == 200


def test_chat_fallback_mode():
    r = client.post("/api/chat", json={"message": "What is address reuse?", "context": ""})
    assert r.status_code == 200
    assert "reuse" in r.json()["answer"].lower()


def test_ai_fallback_no_crash():
    ans = asyncio.run(_ask("??? gibberish xyz"))
    assert isinstance(ans, str) and len(ans) > 20


async def _ask(q: str):
    from app.services.ai_service import ask_sentinel
    a, _ = await ask_sentinel(q)
    return a


def test_nostr_safety_refuses_keys():
    res = nostr_service.publish_note("here is my nsec1abc private key", "anon")
    assert res["ok"] is False


def test_nostr_publish_and_feed():
    res = nostr_service.publish_note("Privacy tip: fresh addresses!", "tester")
    assert res["ok"] is True
    assert client.get("/api/nostr/feed").status_code == 200
    assert client.get("/api/nostr/status").status_code == 200


def test_health():
    assert client.get("/api/health").json()["status"] == "ok"
