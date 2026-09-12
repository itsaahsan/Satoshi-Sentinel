from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["meta"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "satoshi-sentinel"}
