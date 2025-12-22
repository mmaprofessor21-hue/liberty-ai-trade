# P25-06-04_14-47-51
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Required Core Settings
    PROJECT_NAME: str = "Liberty AI Trade"
    VERSION: str = "2.1.0"
    DEBUG: bool = True
    
    # Environment Secrets
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    SOLANA_RPC_URL: str = "https://api.mainnet-beta.solana.com"
    DEXSCREENER_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379"
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    SENTRY_DSN: str
    PORT: int = 8000

    model_config = ConfigDict(env_file=".env", extra="ignore")
