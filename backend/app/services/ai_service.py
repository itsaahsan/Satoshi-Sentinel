"""Sentinel AI: Gemini/OpenAI when keys exist, else deterministic local fallback."""
from __future__ import annotations
import httpx
from ..config import settings

SYSTEM_PROMPT = (
    "You are Sentinel AI, a Bitcoin privacy education assistant. You explain public blockchain "
    "data responsibly. Never claim to identify wallet owners. Never accuse individuals of crimes. "
    "Clearly distinguish facts, estimates, and possibilities. Prioritize user privacy and security. "
    "Provide educational, actionable explanations."
)

FALLBACK_KB: list[tuple[tuple[str, ...], str]] = [
    (("reuse", "reusing", "address reuse"), (
        "**Address reuse** means receiving multiple payments to the same Bitcoin address.\n\n"
        "Why it matters: every payment to a reused address is trivially linkable — anyone viewing the "
        "blockchain sees one combined history and balance. It also invites clustering with your other "
        "transactions.\n\nWhat to do: use a fresh address per receive (most modern wallets do this "
        "automatically), and keep publicly-posted addresses separate from private savings.")),
    (("coinjoin", "coin join", "mixer", "mixing"), (
        "**CoinJoin** is a collaborative transaction where several users combine inputs/outputs so the "
        "on-chain link between sender and receiver is ambiguous.\n\nTrade-offs: may cost fees, needs "
        "liquidity, and some services treat CoinJoin history cautiously. Study the tool, coordinator trust "
        "model, and your local regulations before use. It is a privacy technique, not anonymity magic.")),
    (("surveillance", "tracking", "chainalysis", "clustering", "monitor"), (
        "Bitcoin **surveillance** typically means blockchain analytics: observers cluster addresses using "
        "heuristics like common-input ownership (inputs in one tx usually share an owner), address reuse, "
        "round amounts, timing patterns, and off-chain leaks (posting an address publicly, exchange KYC, IP "
        "metadata).\n\nCounter-practices: fresh addresses, coin control, separate wallets per purpose, "
        "avoiding public address linkage, and understanding that **amounts, timing, and counterparties are all metadata**.")),
    (("nostr",), (
        "**Nostr** is a decentralized, censorship-resistant messaging protocol built on relays and public-key "
        "identities (npub/nsec). No accounts, no central server.\n\nIn Satoshi Sentinel it carries *educational* "
        "privacy alerts — never sensitive balances or keys. You can generate a demo identity or paste an npub, "
        "connect to a relay like relay.damus.io, and publish privacy tips for the community feed.")),
    (("lightning",), (
        "**Lightning Network** moves frequent small payments off-chain through payment channels. Only "
        "channel opens/closes appear on-chain, so day-to-day Lightning payments leave far less public graph "
        "data.\n\nPrivacy notes: routing nodes see forwarding amounts, and channel balances leak slightly over "
        "time — but it is generally much quieter than paying on-chain for every coffee.")),
    (("utxo",), (
        "**UTXOs** (unspent transaction outputs) are the chunks of bitcoin your wallet holds — like digital "
        "banknotes. Spending combines UTXOs as inputs.\n\nPrivacy angle: combining many UTXOs in one transaction "
        "publicly declares they share an owner (common-input heuristic). **Coin control** — choosing which UTXOs "
        "to spend — is a core privacy skill.")),
    (("private", "privacy", "improve", "score", "risk", "footprint", "how private"), (
        "To read your privacy report: the **score (0–100)** blends address reuse, counterparty count, frequency, "
        "public exposure, and clustering signals. Higher = more contained footprint.\n\nGeneral improvements: "
        "(1) fresh address per receive, (2) separate wallets for savings/spending/public, (3) avoid posting "
        "addresses publicly, (4) learn coin control, (5) consider Lightning for small frequent spends. "
        "This is an educational estimate, not forensic certainty.")),
    (("scam", "suspicious", "fraud", "phishing"), (
        "I can't label any transaction a scam from on-chain data alone — but be cautious of: unsolicited "
        "'double your BTC' offers, dust outputs paired with phishing links, impersonator donation addresses, "
        "and anyone asking for your **seed phrase or private keys** (always a scam — Sentinel never asks).\n\n"
        "Verify addresses out-of-band and treat unexpected deposits with suspicion.")),
    (("self-custody", "custody", "seed", "hardware", "wallet"), (
        "**Self-custody** means you hold your own keys (e.g. hardware wallet + written seed backup). No "
        "exchange can freeze it — but no one can recover it either.\n\nBasics: buy from reputable vendors, "
        "verify receive addresses on-device, keep seed offline on paper/steel, never photograph it, and "
        "practice small test transactions first.")),
]


def local_answer(question: str, context: str = "") -> str:
    q = (question or "").lower()
    for keywords, answer in FALLBACK_KB:
        if any(k in q for k in keywords):
            prefix = f"{context}\n\n" if context else ""
            return prefix + answer + "\n\n*Answered in offline demo mode — educational only, not financial/legal advice.*"
    prefix = f"{context}\n\n" if context else ""
    return (prefix + "Good question. In short: Bitcoin's ledger is **public**, so privacy comes from "
            "limiting what gets linked — fresh addresses, separated wallets, careful UTXO use, and avoiding "
            "public address exposure.\n\nAsk me about **address reuse**, **CoinJoin**, **UTXOs**, **Lightning**, "
            "**surveillance**, **Nostr**, or paste a scan summary for a personalized explanation."
            "\n\n*Answered in offline demo mode — educational only.*")


async def ask_sentinel(question: str, context: str = "") -> tuple[str, str]:
    """Returns (answer, provider): provider in gemini|openai|local."""
    q = f"{SYSTEM_PROMPT}\n\nUser context: {context}\n\nUser: {question}" if context else f"{SYSTEM_PROMPT}\n\nUser: {question}"
    # Gemini
    if settings.gemini_api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.ai_model}:generateContent?key={settings.gemini_api_key}"
            async with httpx.AsyncClient(timeout=25) as client:
                r = await client.post(url, json={"contents": [{"parts": [{"text": q}]}]})
                if r.status_code == 200:
                    parts = r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    text = "".join(p.get("text", "") for p in parts).strip()
                    if text:
                        return text, "gemini"
        except Exception:
            pass
    # OpenAI-compatible
    if settings.openai_api_key:
        try:
            async with httpx.AsyncClient(timeout=25) as client:
                r = await client.post(
                    f"{settings.openai_base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                    json={"model": "gpt-4o-mini", "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": (context + "\n\n" + question) if context else question}]},
                )
                if r.status_code == 200:
                    text = r.json()["choices"][0]["message"]["content"].strip()
                    if text:
                        return text, "openai"
        except Exception:
            pass
    return local_answer(question, context), "local"


def explain_transaction(tx: dict, wallet_address: str = "") -> str:
    txid = tx.get("txid", "unknown")
    direction = tx.get("direction", "observed")
    amount = tx.get("amount_btc", "?")
    cp = tx.get("counterparty", "another address")
    label = tx.get("label", "")
    return (
        f"This transaction (`{txid}`) moved **{amount} BTC** {direction} "
        f"{'from' if direction == 'received' else 'to' if direction == 'sent' else 'involving'} `{cp}`. "
        f"{label + '. ' if label else ''}"
        f"This single transaction alone does not prove ownership or identity. However, if the same addresses "
        f"appear repeatedly, observers may infer patterns that reduce privacy. "
        f"Educational note only — not an accusation."
    )
