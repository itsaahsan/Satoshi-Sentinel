"""Satoshi Sentinel API — educational Bitcoin privacy analysis. Never handles keys."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.routes_scan import router as scan_router
from .api.routes_chat import router as chat_router
from .api.routes_nostr import router as nostr_router
from .api.routes_transactions import router as meta_router

app = FastAPI(title=settings.app_name, version=settings.app_version,
              description="AI-powered Bitcoin privacy education. No keys, no seeds, no transactions.")

origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()] or ["*"]
if "*" in origins:
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
else:
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                       allow_methods=["*"], allow_headers=["*"])

app.include_router(scan_router)
app.include_router(chat_router)
app.include_router(nostr_router)
app.include_router(meta_router)


@app.get("/")
async def root():
    return {"service": settings.app_name, "version": settings.app_version,
            "disclaimer": "Educational privacy analysis tool. Does not identify wallet owners; no financial/legal advice."}
