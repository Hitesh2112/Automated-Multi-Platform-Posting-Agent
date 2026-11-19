"""
LinkedIn Share API / UGC Post API integration adapter.
"""
import httpx

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class LinkedInPlatform(BasePlatform):
    """Publishes a public post to LinkedIn via UGC Posts API."""

    @property
    def platform_name(self) -> str:
        return "LinkedIn"

    def is_configured(self) -> bool:
        return bool(settings.LINKEDIN_ACCESS_TOKEN)

    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        api_url = "https://api.linkedin.com/v2/ugcPosts"
        person_urn = settings.LINKEDIN_PERSON_URN or "me"
        author_urn = person_urn if person_urn.startswith("urn:li:") else f"urn:li:person:{person_urn}"

        headers = {
            "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }

        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": cta_url,
                            "title": {"text": "Learn More"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        response = await client.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()

        post_id = data.get("id")
        if not post_id:
            return self._failure_result("LinkedIn API returned success without post URN")

        posted_url = f"https://www.linkedin.com/feed/update/{post_id}"
        return self._success_result(posted_url=posted_url, public_access=True)

    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        mock_id = 7129000000000000000 + (abs(hash(message)) % 9999999999)
        return self._success_result(
            posted_url=f"https://www.linkedin.com/feed/update/urn:li:ugcPost:{mock_id}",
            public_access=True,
        )
