"""
GitHub Gist REST API integration adapter.
"""
import httpx

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class GitHubPlatform(BasePlatform):
    """Publishes a public announcement Gist via GitHub REST API."""

    @property
    def platform_name(self) -> str:
        return "GitHub Gist"

    def is_configured(self) -> bool:
        return bool(settings.GITHUB_ACCESS_TOKEN)

    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        api_url = "https://api.github.com/gists"
        headers = {
            "Authorization": f"Bearer {settings.GITHUB_ACCESS_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        content = f"# Announcement\n\n{message}\n\n---\n**Learn More:** [{cta_url}]({cta_url})\n"
        payload = {
            "description": message[:100],
            "public": True,
            "files": {
                "announcement.md": {
                    "content": content,
                }
            },
        }

        response = await client.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()

        html_url = data.get("html_url")
        if not html_url:
            return self._failure_result("GitHub API returned success without Gist URL")

        return self._success_result(posted_url=html_url, public_access=True)

    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        mock_hash = hex(abs(hash(message)) % 0xFFFFFFFFFFFFFFFF)[2:].zfill(16)
        return self._success_result(
            posted_url=f"https://gist.github.com/developer/{mock_hash}",
            public_access=True,
        )
