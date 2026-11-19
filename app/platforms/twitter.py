"""
Twitter / X API v2 integration adapter.
"""
import httpx

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class TwitterPlatform(BasePlatform):
    """Publishes a Tweet via Twitter / X API v2."""

    @property
    def platform_name(self) -> str:
        return "Twitter / X"

    def is_configured(self) -> bool:
        # Requires OAuth 2.0 Bearer Token or Access Token
        return bool(settings.TWITTER_BEARER_TOKEN or settings.TWITTER_ACCESS_TOKEN)

    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        api_url = "https://api.twitter.com/2/tweets"
        token = settings.TWITTER_BEARER_TOKEN or settings.TWITTER_ACCESS_TOKEN
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "text": message,
        }

        response = await client.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()

        tweet_data = data.get("data", {})
        tweet_id = tweet_data.get("id")
        if not tweet_id:
            return self._failure_result("Twitter API returned success without tweet ID")

        posted_url = f"https://x.com/i/web/status/{tweet_id}"
        return self._success_result(posted_url=posted_url, public_access=True)

    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        mock_id = 1858800000000000000 + (abs(hash(message)) % 999999999)
        return self._success_result(
            posted_url=f"https://x.com/tech_corp/status/{mock_id}",
            public_access=True,
        )
