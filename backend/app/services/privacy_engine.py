"""Transparent, educational privacy scoring engine."""
from __future__ import annotations


def clamp(v: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, v))


def score_address_reuse(reuse_count: int, tx_count: int) -> dict:
    """High reuse -> high risk (low sub-score). Returns 0-100 where 100 = best privacy."""
    if tx_count <= 0:
        return {"score": 100, "level": "Low", "detail": "No transactions observed, no reuse detected."}
    ratio = reuse_count / max(tx_count, 1)
    if reuse_count == 0:
        return {"score": 100, "level": "Low", "detail": "No address reuse detected. Good practice."}
    if ratio >= 0.5 or reuse_count >= 20:
        return {"score": max(5, 40 - reuse_count), "level": "High",
                "detail": f"Address reused ~{reuse_count} times across {tx_count} transactions. This may allow observers to link activity together."}
    if ratio >= 0.2 or reuse_count >= 4:
        return {"score": 55, "level": "Medium",
                "detail": f"Some address reuse detected ({reuse_count} times). Consider fresh addresses for new receives."}
    return {"score": 80, "level": "Low", "detail": f"Minor reuse ({reuse_count}). Low but non-zero linking potential."}


def score_counterparties(n: int) -> dict:
    if n <= 3:
        return {"score": 90, "level": "Low", "detail": f"Only {n} counterparties observed. Small observable footprint."}
    if n <= 8:
        return {"score": 65, "level": "Medium", "detail": f"{n} distinct counterparties. Each interaction may add linkable context."}
    return {"score": 35, "level": "High", "detail": f"{n} distinct counterparties. Broad interaction graph increases clustering potential."}


def score_frequency(freq_per_week: float) -> dict:
    if freq_per_week < 1:
        return {"score": 90, "level": "Low", "detail": "Low transaction frequency."}
    if freq_per_week < 5:
        return {"score": 65, "level": "Medium", "detail": f"~{freq_per_week}/week. Regular patterns may become fingerprintable."}
    return {"score": 35, "level": "High", "detail": f"~{freq_per_week}/week. High-frequency patterns may reveal behavioral routines."}


def score_public_exposure(exposed: bool, known_hits: int) -> dict:
    if not exposed and known_hits == 0:
        return {"score": 95, "level": "Low", "detail": "No known public exposure of this address."}
    if known_hits >= 5 or exposed:
        base = 30 if known_hits >= 3 else 50
        return {"score": base, "level": "High" if base <= 40 else "Medium",
                "detail": "Address appears publicly shared or linked to known entities. Anyone can look up its history."}
    return {"score": 60, "level": "Medium", "detail": "Possible limited public exposure."}


def score_clustering(tx_count: int, counterparties: int, reuse_count: int) -> dict:
    signals = (1 if tx_count > 10 else 0) + (1 if counterparties > 6 else 0) + (1 if reuse_count > 3 else 0)
    if signals >= 3:
        return {"score": 30, "level": "High", "detail": "Multiple clustering indicators present. Common-input and reuse heuristics may link transactions."}
    if signals == 2:
        return {"score": 55, "level": "Medium", "detail": "Some clustering indicators present."}
    if signals == 1:
        return {"score": 75, "level": "Low", "detail": "Weak clustering signal."}
    return {"score": 95, "level": "Low", "detail": "No strong clustering indicators."}


WEIGHTS = {"reuse": 0.30, "counterparties": 0.20, "frequency": 0.15, "exposure": 0.20, "clustering": 0.15}


def analyze_wallet(stats: dict) -> dict:
    """stats: tx_count, counterparties, reuse_count, public_exposure, frequency_per_week, known_entity_hits"""
    tx_count = int(stats.get("tx_count", 0))
    counterparties = int(stats.get("counterparties", 0))
    reuse_count = int(stats.get("reuse_count", 0))
    exposed = bool(stats.get("public_exposure", False))
    freq = float(stats.get("frequency_per_week", 0))
    hits = int(stats.get("known_entity_hits", 0))

    categories = {
        "address_reuse": score_address_reuse(reuse_count, tx_count),
        "counterparties": score_counterparties(counterparties),
        "frequency": score_frequency(freq),
        "public_exposure": score_public_exposure(exposed, hits),
        "clustering": score_clustering(tx_count, counterparties, reuse_count),
    }
    overall = round(
        categories["address_reuse"]["score"] * WEIGHTS["reuse"]
        + categories["counterparties"]["score"] * WEIGHTS["counterparties"]
        + categories["frequency"]["score"] * WEIGHTS["frequency"]
        + categories["public_exposure"]["score"] * WEIGHTS["exposure"]
        + categories["clustering"]["score"] * WEIGHTS["clustering"]
    )
    overall = int(clamp(overall))
    if overall >= 70:
        band, summary = "low", "Relatively contained on-chain footprint based on available data."
    elif overall >= 45:
        band, summary = "medium", "Moderate privacy considerations worth reviewing."
    else:
        band, summary = "high", "Several potential privacy risks detected. Review recommendations."
    concerns: list[str] = []
    for key, c in categories.items():
        if c["level"] in ("High", "Medium"):
            concerns.append(f"{key.replace('_', ' ').title()}: {c['detail']}")
    return {
        "overall_score": overall, "risk_band": band, "summary": summary,
        "categories": categories, "concerns": concerns,
        "disclaimer": "Educational estimate only — not forensic certainty. Does not identify owners.",
    }


def build_recommendations(report: dict, stats: dict) -> list[dict]:
    recs: list[dict] = []
    cats = report["categories"]
    if cats["address_reuse"]["level"] in ("High", "Medium"):
        recs.append({"title": "Avoid reusing receiving addresses", "priority": "high",
                     "detail": "Use a fresh address for each receive where your wallet supports it. Reuse lets any observer link all payments to one place."})
    if cats["public_exposure"]["level"] in ("High", "Medium"):
        recs.append({"title": "Separate public and private funds", "priority": "high",
                     "detail": "If an address was posted publicly (donations, social media), avoid sending private funds through it. Consider a separate wallet for public receives."})
    if cats["clustering"]["level"] in ("High", "Medium"):
        recs.append({"title": "Learn UTXO management", "priority": "medium",
                     "detail": "Combining many inputs in one transaction can link them. Learn coin control and avoid unnecessary consolidation."})
    if cats["counterparties"]["level"] in ("High", "Medium"):
        recs.append({"title": "Compartmentalize wallets by purpose", "priority": "medium",
                     "detail": "Use separate wallets for savings, spending, and public activity to limit cross-linking."})
    if cats["frequency"]["level"] in ("High", "Medium"):
        recs.append({"title": "Vary timing and amounts thoughtfully", "priority": "low",
                     "detail": "Highly regular patterns can be fingerprintable. Avoid needless automation metadata."})
    recs.append({"title": "Explore Lightning & CoinJoin concepts", "priority": "low",
                 "detail": "Study Lightning for frequent small payments and collaborative transactions (e.g. CoinJoin) — understand trade-offs before use."})
    recs.append({"title": "Never share seeds or keys", "priority": "high",
                 "detail": "No legitimate privacy tool will ask for your seed phrase or private keys. Satoshi Sentinel never does."})
    return recs
