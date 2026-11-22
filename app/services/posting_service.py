"""
Service orchestrator for asynchronous multi-platform posting.
"""
import asyncio
import logging
import time
from typing import List, Optional
import httpx

from app.config import settings
from app.logger import (
    log_broadcast_start,
    log_broadcast_summary,
    log_platform_dispatch_result,
)
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
        total_start = time.perf_counter()

        # Visual dispatch banner
        log_broadcast_start(
            platforms_count=len(self.platforms),
            message=message,
            cta_url=cta_url,
            is_mock=settings.MOCK_MODE,
        )

        async def _timed_post(platform: BasePlatform):
            t0 = time.perf_counter()
            try:
                res = await platform.post(message=message, cta_url=cta_url, client=client)
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                return res, elapsed_ms
            except Exception as exc:
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                return exc, elapsed_ms

        # Create concurrent coroutines for each platform
        tasks = [_timed_post(p) for p in self.platforms]

        # Execute concurrently with complete exception isolation
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        results: List[PlatformResult] = []
        for platform, item in zip(self.platforms, raw_results):
            if isinstance(item, tuple):
                res, elapsed_ms = item
            else:
                res, elapsed_ms = item, 0.0

            if isinstance(res, Exception):
                logger.error("Unhandled exception escaped platform %s: %s", platform.platform_name, res)
                result_obj = PlatformResult(
                    platform=platform.platform_name,
                    status="failed",
                    posted_url=None,
                    public_access=False,
                    date=None,
                    time=None,
                    error=f"Unexpected error: {str(res)}",
                )
            elif isinstance(res, PlatformResult):
                result_obj = res
            else:
                logger.error("Unknown result type from platform %s: %s", platform.platform_name, type(res))
                result_obj = PlatformResult(
                    platform=platform.platform_name,
                    status="failed",
                    error="Unknown error",
                )

            # Log individual platform completion with visual icon, badge, and latency
            log_platform_dispatch_result(
                platform_name=result_obj.platform,
                status=result_obj.status,
                url_or_error=result_obj.posted_url if result_obj.status == "success" else result_obj.error,
                elapsed_ms=elapsed_ms,
            )
            results.append(result_obj)

        total_ms = (time.perf_counter() - total_start) * 1000.0
        succeeded_count = sum(1 for r in results if r.status == "success")
        failed_count = len(results) - succeeded_count

        # Log completion summary
        log_broadcast_summary(
            total=len(results),
            succeeded=succeeded_count,
            failed=failed_count,
            total_ms=total_ms,
        )

        overall_success = succeeded_count > 0

        return PostingResponse(success=overall_success, results=results)
