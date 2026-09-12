from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    address: str = Field(..., min_length=3, max_length=120)
    mode: str = "demo"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: str = ""


class ExplainRequest(BaseModel):
    tx: dict = {}
    wallet_address: str = ""


class PublishRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=280)
    author: str = "anonymous"
