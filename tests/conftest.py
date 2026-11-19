"""
Pytest configuration and shared fixtures.
"""
from typing import AsyncGenerator
import httpx
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Synchronous FastAPI TestClient with lifespan events executed."""
    with TestClient(app) as test_client:
        yield test_client


@pytest_asyncio.fixture
async def async_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Async HTTPX client for direct platform adapter testing."""
    async with httpx.AsyncClient() as http_client:
        yield http_client


@pytest.fixture
def enable_mock_mode():
    """Context fixture to temporarily force MOCK_MODE = True."""
    prev = settings.MOCK_MODE
    settings.MOCK_MODE = True
    yield
    settings.MOCK_MODE = prev


@pytest.fixture
def disable_mock_mode():
    """Context fixture to temporarily force MOCK_MODE = False."""
    prev = settings.MOCK_MODE
    settings.MOCK_MODE = False
    yield
    settings.MOCK_MODE = prev
