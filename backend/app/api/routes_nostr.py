from fastapi import APIRouter
from ..schemas.requests import PublishRequest
from ..services import nostr_service

router = APIRouter(prefix="/api/nostr", tags=["nostr"])


@router.get("/status")
async def status():
    return nostr_service.relay_status()


@router.get("/identity")
async def identity():
    return nostr_service.generate_demo_identity()


@router.get("/feed")
async def feed():
    return {"posts": nostr_service.get_feed(), "relay": nostr_service.relay_status()["relay"]}


@router.post("/publish")
async def publish(req: PublishRequest):
    result = nostr_service.publish_note(req.content, req.author)
    if not result.get("ok"):
        return {"ok": False, "error": result.get("error")}
    return result
