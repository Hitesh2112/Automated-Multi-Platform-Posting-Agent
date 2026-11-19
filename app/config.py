"""
Application configuration and environment variables using Pydantic Settings.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application runtime settings."""

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 4000
    DEBUG: bool = False

    # Evaluation / Simulation Mode
    # If True, platforms without live credentials generate realistic successful posts.
    # If False, unconfigured platforms return "Authentication failed" per test requirements.
    MOCK_MODE: bool = False

    # HTTP Client Timeout
    REQUEST_TIMEOUT_SECONDS: float = 10.0

    # Telegram Credentials
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    # Twitter / X Credentials (API v2)
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None

    # LinkedIn Credentials (UGC Post API)
    LINKEDIN_ACCESS_TOKEN: Optional[str] = None
    LINKEDIN_PERSON_URN: Optional[str] = None

    # Reddit Credentials (OAuth2 API)
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USERNAME: Optional[str] = None
    REDDIT_PASSWORD: Optional[str] = None
    REDDIT_SUBREDDIT: str = "test"

    # GitHub Credentials (Gist API)
    GITHUB_ACCESS_TOKEN: Optional[str] = None

    # Meta Threads / Instagram Credentials
    THREADS_ACCESS_TOKEN: Optional[str] = None
    THREADS_USER_ID: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
