"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
import httpx

from app.config import settings
from app.error_handlers import register_error_handlers
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("multi_platform_posting.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan resources (e.g. shared HTTP connection pool)."""
    logger.info("Initializing HTTPX connection pool...")
    limits = httpx.Limits(max_keepalive_connections=20, max_connections=50)
    async with httpx.AsyncClient(limits=limits, timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
        app.state.http_client = client
        app.state.posting_service = PostingService()
        logger.info("Server started successfully. Registered platforms: %d", len(app.state.posting_service.platforms))
        yield
    logger.info("Shutting down HTTPX connection pool...")


app = FastAPI(
    title="Multi-Platform Automated Posting System",
    description=(
        "Production-grade FastAPI application that automatically publishes short messages "
        "across multiple third-party social, professional, forum, and developer platforms "
        "through their official REST APIs with asynchronous concurrency and isolated error boundaries."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS for interactive testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
register_error_handlers(app)


@app.get(
    "/health",
    summary="Health Check",
    tags=["System"],
)
async def health_check():
    """Health check endpoint to verify service availability and configuration status."""
    return {
        "status": "healthy",
        "mock_mode": settings.MOCK_MODE,
        "platforms_count": len(app.state.posting_service.platforms) if hasattr(app.state, "posting_service") else 0,
    }


@app.post(
    "/posting",
    response_model=PostingResponse,
    status_code=status.HTTP_200_OK,
    summary="Publish short message to multiple platforms",
    description=(
        "Concurrently publishes a short message (max 200 characters with exactly one valid CTA link) "
        "across all supported platforms: Twitter / X, LinkedIn, Reddit, Telegram, GitHub Gist, "
        "and Instagram Threads. Handles failures independently without stopping other platforms."
    ),
    tags=["Posting"],
)
async def post_message(
    payload: PostingRequest,
    request: Request,
) -> PostingResponse:
    """
    Main posting endpoint. Validates input, coordinates asynchronous posting,
    and returns comprehensive execution details per platform.
    """
    http_client: httpx.AsyncClient = request.app.state.http_client
    posting_service: PostingService = request.app.state.posting_service

    return await posting_service.post_to_all(
        message=payload.message,
        cta_url=payload.cta_url,
        client=http_client,
    )
