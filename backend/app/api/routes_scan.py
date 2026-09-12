from fastapi import APIRouter, HTTPException
from ..schemas.requests import ScanRequest
from ..services.bitcoin_service import get_wallet_stats
from ..services.privacy_engine import analyze_wallet, build_recommendations
from ..services.demo_data import DEMO_WALLETS

router = APIRouter(prefix="/api/scan", tags=["scan"])


@router.post("")
async def scan_wallet(req: ScanRequest):
    address = req.address.strip()
    if not address:
        raise HTTPException(400, "Address is required.")
    mode = req.mode if req.mode in ("demo", "live") else "demo"
    stats, source = await get_wallet_stats(address, mode)
    report = analyze_wallet(stats)
    recs = build_recommendations(report, stats)
    return {
        "address": address, "mode": mode, "source": source,
        "label": stats.get("label", "Wallet"),
        "score": report["overall_score"], "risk_band": report["risk_band"],
        "summary": report["summary"], "categories": report["categories"],
        "concerns": report["concerns"], "recommendations": recs,
        "transactions": stats.get("transactions", []),
        "graph": stats.get("graph", {"nodes": [], "edges": []}),
        "stats": {"tx_count": stats.get("tx_count"), "counterparties": stats.get("counterparties"),
                  "reuse_count": stats.get("reuse_count")},
        "disclaimer": report["disclaimer"],
    }


@router.get("/demos")
async def list_demos():
    return [{"key": k, "address": v["address"], "label": v["label"], "expected_score": v["expected_score"],
             "summary": v["summary"]} for k, v in DEMO_WALLETS.items()]
