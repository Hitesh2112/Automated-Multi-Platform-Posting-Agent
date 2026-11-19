"""
Base class definition for all third-party platform integrations.
"""
from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import Optional
import httpx

from app.config import settings
from app.schemas import PlatformResult

logger = logging.getLogger("multi_platform_posting.platforms")


class BasePlatform(ABC):
    """Abstract base class that all platform adapters must implement."""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Human-readable platform name."""
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check whether the necessary API credentials are provided in configuration."""
        pass

    @abstractmethod
    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        """Perform the actual platform-specific API call."""
        pass

    @abstractmethod
    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        """Generate a realistic mock result for evaluation when MOCK_MODE is enabled."""
        pass

    async def post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        """
        Public posting entry point with unified error isolation,
        credential checking, and mock fallback.
        """
        # If credentials are not configured
        if not self.is_configured():
            if settings.MOCK_MODE:
                logger.info("[%s] Running in MOCK_MODE (no credentials configured)", self.platform_name)
                return self._generate_mock_result(message, cta_url)

            logger.warning("[%s] API credentials not configured in environment", self.platform_name)
            return self._failure_result("Authentication failed: Missing API credentials")

        try:
            return await self._execute_post(message, cta_url, client)
        except httpx.TimeoutException as exc:
            logger.error("[%s] Request timed out: %s", self.platform_name, exc)
            return self._failure_result("Request timed out after configured threshold")
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            error_body = exc.response.text[:200]
            logger.error("[%s] Remote API HTTP %s: %s", self.platform_name, status_code, error_body)
            if status_code in (401, 403):
                return self._failure_result(f"Authentication failed: Remote rejected credentials (HTTP {status_code})")
            elif status_code == 429:
                return self._failure_result("Rate limit exceeded on remote platform. Please try again later.")
            return self._failure_result(f"Remote API error (HTTP {status_code}): {error_body}")
        except httpx.RequestError as exc:
            logger.error("[%s] Connection error: %s", self.platform_name, exc)
            return self._failure_result(f"Network error: Unable to connect to platform API ({type(exc).__name__})")
        except Exception as exc:
            logger.exception("[%s] Unexpected error during posting: %s", self.platform_name, exc)
            return self._failure_result(f"Internal error: {str(exc)}")

    def _success_result(self, posted_url: str, public_access: bool = True) -> PlatformResult:
        """Construct a standardized successful PlatformResult."""
        now = datetime.now()
        return PlatformResult(
            platform=self.platform_name,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            error=None,
        )

    def _failure_result(self, error_message: str) -> PlatformResult:
        """Construct a standardized failed PlatformResult."""
        return PlatformResult(
            platform=self.platform_name,
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error=error_message,
        )
