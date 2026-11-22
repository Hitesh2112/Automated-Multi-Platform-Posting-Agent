"""
Unit tests for individual platform adapters covering authentication,
success parsing, HTTP error states, and mock fallback.
"""
import httpx
import pytest
import respx

from app.config import settings
from app.platforms.github import GitHubPlatform
from app.platforms.instagram_threads import InstagramThreadsPlatform
from app.platforms.linkedin import LinkedInPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.twitter import TwitterPlatform


@pytest.mark.asyncio
class TestPlatformAdapters:
    """Test suite for the 6 individual platform adapters."""

    async def test_telegram_unconfigured_auth_failure(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "TELEGRAM_BOT_TOKEN", None)
        monkeypatch.setattr(settings, "TELEGRAM_CHAT_ID", None)
        platform = TelegramPlatform()
        result = await platform.post("Test message https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert result.posted_url is None
        assert result.public_access is False
        assert "Authentication failed" in (result.error or "")

    async def test_telegram_mock_mode(self, enable_mock_mode, async_http_client):
        platform = TelegramPlatform()
        result = await platform.post("Test message https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert result.posted_url is not None
        assert "t.me" in result.posted_url
        assert result.public_access is True
        assert result.date is not None
        assert result.time is not None

    @respx.mock
    async def test_telegram_live_success(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "TELEGRAM_BOT_TOKEN", "fake_token_123")
        monkeypatch.setattr(settings, "TELEGRAM_CHAT_ID", "@my_public_channel")

        respx.post("https://api.telegram.org/botfake_token_123/sendMessage").respond(
            200,
            json={
                "ok": True,
                "result": {
                    "message_id": 999,
                    "chat": {"username": "my_public_channel", "title": "My Channel"},
                },
            },
        )

        platform = TelegramPlatform()
        result = await platform.post("Test https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert result.posted_url == "https://t.me/my_public_channel/999"
        assert result.public_access is True

    async def test_twitter_unconfigured_auth_failure(self, disable_mock_mode, async_http_client):
        platform = TwitterPlatform()
        result = await platform.post("Tweet https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert "Authentication failed" in (result.error or "")

    async def test_twitter_mock_mode(self, enable_mock_mode, async_http_client):
        platform = TwitterPlatform()
        result = await platform.post("Tweet https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert "x.com" in result.posted_url

    @respx.mock
    async def test_twitter_live_success(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "TWITTER_BEARER_TOKEN", "fake_bearer_abc")

        respx.post("https://api.twitter.com/2/tweets").respond(
            201,
            json={"data": {"id": "1858827391029384712", "text": "Tweet https://example.com"}},
        )

        platform = TwitterPlatform()
        result = await platform.post("Tweet https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert result.posted_url == "https://x.com/i/web/status/1858827391029384712"

    async def test_linkedin_unconfigured_auth_failure(self, disable_mock_mode, async_http_client):
        platform = LinkedInPlatform()
        result = await platform.post("Post https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert "Authentication failed" in (result.error or "")

    @respx.mock
    async def test_linkedin_live_success(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "LINKEDIN_ACCESS_TOKEN", "fake_li_token")
        monkeypatch.setattr(settings, "LINKEDIN_PERSON_URN", "urn:li:person:12345")

        respx.post("https://api.linkedin.com/v2/ugcPosts").respond(
            201,
            json={"id": "urn:li:ugcPost:7129384729103847192"},
        )

        platform = LinkedInPlatform()
        result = await platform.post("Post https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert result.posted_url == "https://www.linkedin.com/feed/update/urn:li:ugcPost:7129384729103847192"

    async def test_reddit_unconfigured_auth_failure(self, disable_mock_mode, async_http_client):
        platform = RedditPlatform()
        result = await platform.post("Reddit https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert "Authentication failed" in (result.error or "")

    @respx.mock
    async def test_reddit_live_success(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "REDDIT_CLIENT_ID", "fake_cid")
        monkeypatch.setattr(settings, "REDDIT_CLIENT_SECRET", "fake_csec")
        monkeypatch.setattr(settings, "REDDIT_USERNAME", "testuser")
        monkeypatch.setattr(settings, "REDDIT_PASSWORD", "testpass")
        monkeypatch.setattr(settings, "REDDIT_SUBREDDIT", "test")

        respx.post("https://www.reddit.com/api/v1/access_token").respond(
            200,
            json={"access_token": "fake_reddit_token", "token_type": "bearer"},
        )
        respx.post("https://oauth.reddit.com/api/submit").respond(
            200,
            json={
                "json": {
                    "errors": [],
                    "data": {
                        "url": "https://www.reddit.com/r/test/comments/1gx9abc/announcement/",
                        "id": "1gx9abc",
                    },
                }
            },
        )

        platform = RedditPlatform()
        result = await platform.post("Announcement https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert "reddit.com" in result.posted_url

    async def test_github_unconfigured_auth_failure(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "GITHUB_ACCESS_TOKEN", None)
        platform = GitHubPlatform()
        result = await platform.post("Gist https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert "Authentication failed" in (result.error or "")

    @respx.mock
    async def test_github_live_success(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "GITHUB_ACCESS_TOKEN", "ghp_fake_token")

        respx.post("https://api.github.com/gists").respond(
            201,
            json={"html_url": "https://gist.github.com/octocat/8f3a9b1c7e2d"},
        )

        platform = GitHubPlatform()
        result = await platform.post("Gist https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert result.posted_url == "https://gist.github.com/octocat/8f3a9b1c7e2d"
        assert result.public_access is True

    async def test_threads_unconfigured_auth_failure(self, disable_mock_mode, async_http_client):
        platform = InstagramThreadsPlatform()
        result = await platform.post("Threads https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert "Authentication failed" in (result.error or "")

    @respx.mock
    async def test_threads_live_success(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "THREADS_ACCESS_TOKEN", "fake_threads_token")
        monkeypatch.setattr(settings, "THREADS_USER_ID", "user_12345")

        respx.post("https://graph.threads.net/v1.0/user_12345/threads").respond(
            200,
            json={"id": "container_999"},
        )
        respx.post("https://graph.threads.net/v1.0/user_12345/threads_publish").respond(
            200,
            json={"id": "thread_888"},
        )

        platform = InstagramThreadsPlatform()
        result = await platform.post("Threads post https://example.com", "https://example.com", async_http_client)
        assert result.status == "success"
        assert result.posted_url == "https://www.threads.net/@post/thread_888"

    @respx.mock
    async def test_platform_timeout_handling(self, disable_mock_mode, async_http_client, monkeypatch):
        monkeypatch.setattr(settings, "GITHUB_ACCESS_TOKEN", "ghp_fake_token")
        respx.post("https://api.github.com/gists").mock(side_effect=httpx.TimeoutException("Read timeout"))

        platform = GitHubPlatform()
        result = await platform.post("Gist https://example.com", "https://example.com", async_http_client)
        assert result.status == "failed"
        assert "timed out" in (result.error or "").lower()
