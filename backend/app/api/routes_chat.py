from fastapi import APIRouter
from ..schemas.requests import ChatRequest, ExplainRequest
from ..services.ai_service import ask_sentinel, explain_transaction

router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/chat")
async def chat(req: ChatRequest):
    answer, provider = await ask_sentinel(req.message, req.context)
    return {"answer": answer, "provider": provider}


@router.post("/explain")
async def explain(req: ExplainRequest):
    return {"explanation": explain_transaction(req.tx, req.wallet_address), "provider": "local"}
