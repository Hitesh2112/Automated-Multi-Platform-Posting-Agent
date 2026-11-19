"""
Service orchestrator for asynchronous multi-platform posting.
"""
import asyncio
import logging
from typing import List, Optional
import httpx

from app.platforms.base import BasePlatform
from app.platforms.registry import get_all_platforms
from app.schemas import PlatformResult, PostingResponse

logger = logging.getLogger("multi_platform_posting.service")


class PostingService:
    """Orchestrates asynchronous publishing across multiple platforms concurrently."""

    def __init__(self, platforms: Optional[List[BasePlatform]] = None):
        self.platforms = platforms if platforms is not None else get_all_platforms()

    async def post_to_all(
        self,
        message: str,
        cta_url: str,
        client: httpx.AsyncClient,
    ) -> PostingResponse:
        """
        Concurrently publish the message and CTA URL to all registered platforms.
        Guarantees that a failure on one platform does not block or cancel others.
        """
        logger.info(
            "Initiating multi-platform posting for %d platforms. Message length: %d",
            len(self.platforms),
            len(message),
        )

        # Create concurrent coroutines for each platform
        tasks = [
            platform.post(message=message, cta_url=cta_url, client=client)
            for platform in self.platforms
        ]

        # Execute concurrently with complete exception isolation
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        results: List[PlatformResult] = []
        for platform, res in zip(self.platforms, raw_results):
            if isinstance(res, Exception):
                logger.error("Unhandled exception escaped platform %s: %s", platform.platform_name, res)
                results.append(
                    PlatformResult(
                        platform=platform.platform_name,
                        status="failed",
                        posted_url=None,
                        public_access=False,
                        date=None,
                        time=None,
                        error=f"Unexpected error: {str(res)}",
                    )
                )
            elif isinstance(res, PlatformResult):
                results.append(res)
            else:
                logger.error("Unknown result type from platform %s: %s", platform.platform_name, type(res))
                results.append(
                    PlatformResult(
                        platform=platform.platform_name,
                        status="failed",
                        error="Unknown error",
                    )
                )

        # Overall success is true if at least one platform succeeded, or if execution ran cleanly
        overall_success = any(r.status == "success" for r in results)

        logger.info(
            "Posting completed. Successful platforms: %d / %d",
            sum(1 for r in results if r.status == "success"),
            len(results),
        )

        return PostingResponse(success=overall_success, results=results)
