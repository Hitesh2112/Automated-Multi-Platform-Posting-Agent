"""
Reddit OAuth2 API integration adapter.
"""
import httpx

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class RedditPlatform(BasePlatform):
    """Submits a post or link to a subreddit via Reddit OAuth2 API."""

    @property
    def platform_name(self) -> str:
        return "Reddit"

    def is_configured(self) -> bool:
        return bool(
            settings.REDDIT_CLIENT_ID
            and settings.REDDIT_CLIENT_SECRET
            and settings.REDDIT_USERNAME
            and settings.REDDIT_PASSWORD
        )

    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        # Step 1: Obtain OAuth2 Bearer Token
        token_url = "https://www.reddit.com/api/v1/access_token"
        user_agent = f"python:multi-platform-poster:v1.0.0 (by /u/{settings.REDDIT_USERNAME})"

        auth = (settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET)
        token_data = {
            "grant_type": "password",
            "username": settings.REDDIT_USERNAME,
            "password": settings.REDDIT_PASSWORD,
        }
        token_headers = {"User-Agent": user_agent}

        token_resp = await client.post(
            token_url,
            auth=auth,
            data=token_data,
            headers=token_headers,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        token_resp.raise_for_status()
        token_json = token_resp.json()
        access_token = token_json.get("access_token")

        if not access_token:
            return self._failure_result("Authentication failed: Reddit OAuth did not return access token")

        # Step 2: Submit link/post to subreddit
        submit_url = "https://oauth.reddit.com/api/submit"
        headers = {
            "Authorization": f"bearer {access_token}",
            "User-Agent": user_agent,
        }

        # Create a title from message, up to 100 chars
        title = message.split(cta_url)[0].strip() or message[:80]
        if not title:
            title = "New Update"

        payload = {
            "sr": settings.REDDIT_SUBREDDIT,
            "kind": "link",
            "title": title[:100],
            "url": cta_url,
            "resubmit": "true",
            "sendreplies": "true",
        }

        submit_resp = await client.post(
            submit_url,
            headers=headers,
            data=payload,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        submit_resp.raise_for_status()
        data = submit_resp.json()

        json_block = data.get("json", {})
        errors = json_block.get("errors", [])
        if errors:
            error_details = "; ".join(str(e) for e in errors)
            return self._failure_result(f"Reddit submission error: {error_details}")

        result_data = json_block.get("data", {})
        posted_url = result_data.get("url")

        if not posted_url:
            post_id = result_data.get("id")
            if post_id:
                posted_url = f"https://www.reddit.com/r/{settings.REDDIT_SUBREDDIT}/comments/{post_id}/"
            else:
                return self._failure_result("Reddit API succeeded but returned no post URL")

        return self._success_result(posted_url=posted_url, public_access=True)

    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        mock_id = hex(abs(hash(message)) % 0xFFFFFF)[2:]
        return self._success_result(
            posted_url=f"https://www.reddit.com/r/{settings.REDDIT_SUBREDDIT}/comments/{mock_id}/announcement/",
            public_access=True,
        )
