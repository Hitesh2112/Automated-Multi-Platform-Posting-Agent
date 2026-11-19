"""
Instagram / Meta Threads API integration adapter.
"""
import httpx

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class InstagramThreadsPlatform(BasePlatform):
    """
    Publishes text and CTA links via the official Meta Threads API
    (Instagram's text-based social conversation platform).
    """

    @property
    def platform_name(self) -> str:
        return "Instagram Threads"

    def is_configured(self) -> bool:
        return bool(settings.THREADS_ACCESS_TOKEN and settings.THREADS_USER_ID)

    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        user_id = settings.THREADS_USER_ID
        token = settings.THREADS_ACCESS_TOKEN

        # Step 1: Create a Threads text container
        create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
        create_params = {
            "media_type": "TEXT",
            "text": message,
            "access_token": token,
        }

        create_resp = await client.post(
            create_url,
            params=create_params,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        create_resp.raise_for_status()
        create_data = create_resp.json()
        container_id = create_data.get("id")

        if not container_id:
            return self._failure_result("Threads API error: Container creation did not return an ID")

        # Step 2: Publish the container
        publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
        publish_params = {
            "creation_id": container_id,
            "access_token": token,
        }

        publish_resp = await client.post(
            publish_url,
            params=publish_params,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        publish_resp.raise_for_status()
        publish_data = publish_resp.json()
        post_id = publish_data.get("id")

        if not post_id:
            return self._failure_result("Threads API error: Publishing did not return post ID")

        posted_url = f"https://www.threads.net/@post/{post_id}"
        return self._success_result(posted_url=posted_url, public_access=True)

    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        mock_id = (abs(hash(message)) % 900000000) + 100000000
        return self._success_result(
            posted_url=f"https://www.threads.net/@tech_corp/post/DC{mock_id}",
            public_access=True,
        )
