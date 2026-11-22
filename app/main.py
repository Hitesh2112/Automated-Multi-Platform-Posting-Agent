"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
import logging
import time
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx

from app.config import settings
from app.docs import API_GUIDE_HTML, DOCS_HTML
from app.error_handlers import register_error_handlers
from app.logger import setup_logging
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import PostingService

# Initialize visual console + persistent file logging
setup_logging(log_level=logging.INFO, log_file="logs/app.log")
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
    docs_url="/swagger",
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


@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """Log incoming HTTP requests with timing, client IP, and status."""
    start_time = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start_time) * 1000.0

    path = request.url.path
    # Highlight API endpoints cleanly
    if path in ("/posting", "/health") or path.startswith("/api"):
        client_ip = request.client.host if request.client else "unknown"
        status_code = response.status_code
        logger.info(
            "📡 HTTP %s %s ➔ %s (%.1fms) from %s",
            request.method,
            path,
            status_code,
            duration_ms,
            client_ip,
        )
    return response

# Register custom exception handlers
register_error_handlers(app)


@app.get(
    "/docs",
    response_class=HTMLResponse,
    include_in_schema=False,
    summary="Interactive Visual Documentation & Playground",
)
@app.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
    summary="Home Page & Interactive Docs",
)
async def interactive_visual_docs():
    """
    Serve the modern, interactive storytelling documentation and live API playground.
    """
    return HTMLResponse(content=DOCS_HTML)


@app.get(
    "/api-guide",
    response_class=HTMLResponse,
    include_in_schema=False,
    summary="Comprehensive API Keys Setup Guide Page",
)
async def api_keys_setup_guide_page():
    """
    Dedicated documentation page for setting up real platform credentials.
    """
    return HTMLResponse(content=API_GUIDE_HTML)


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
