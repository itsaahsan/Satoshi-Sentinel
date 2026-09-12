"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Satoshi Sentinel"
    app_version: str = "1.0.0"
    debug: bool = True
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    # External APIs (all optional — demo mode works without them)
    gemini_api_key: str = ""
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gemini-2.0-flash"
    mempool_api_url: str = "https://mempool.space/api"
    blockstream_api_url: str = "https://blockstream.info/api"
    bitcoin_mode: str = "demo"  # demo | live
    nostr_default_relay: str = "wss://relay.damus.io"
    database_url: str = "sqlite:///./sentinel.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
