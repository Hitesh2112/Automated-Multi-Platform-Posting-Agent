"""
Integration tests for the POST /posting API endpoint.
"""
from fastapi.testclient import TestClient

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult
from app.services.posting_service import PostingService


class TestPostingEndpoint:
    """End-to-end tests for the /posting endpoint."""

    def test_posting_mock_mode_all_success(self, client: TestClient, enable_mock_mode):
        payload = {
            "message": "Check out our latest business platform and grow your online visibility. https://example.com"
        }
        response = client.post("/posting", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert len(data["results"]) >= 5

        for item in data["results"]:
            assert "platform" in item
            assert item["status"] == "success"
            assert item["posted_url"] is not None
            assert item["public_access"] is True
            assert item["date"] is not None
            assert item["time"] is not None
            assert item["error"] is None

    def test_posting_unconfigured_auth_failure_matches_spec(self, client: TestClient, disable_mock_mode):
        payload = {
            "message": "Check out our latest business platform and grow your online visibility. https://example.com"
        }
        response = client.post("/posting", json=payload)
        assert response.status_code == 200
        data = response.json()

        # In unconfigured mode, all return authentication failed
        assert len(data["results"]) >= 5
        for item in data["results"]:
            assert item["status"] == "failed"
            assert item["posted_url"] is None
            assert item["public_access"] is False
            assert "Authentication failed" in (item["error"] or "")

    def test_partial_failure_isolation(self, client: TestClient, monkeypatch):
        """Simulate a mixed scenario: some platforms succeed, some fail."""

        class MockSuccessPlatform(BasePlatform):
            @property
            def platform_name(self) -> str:
                return "Platform Alpha (Success)"

            def is_configured(self) -> bool:
                return True

            async def _execute_post(self, message, cta_url, client) -> PlatformResult:
                return self._success_result(posted_url="https://alpha.com/post/100", public_access=True)

            def _generate_mock_result(self, message, cta_url) -> PlatformResult:
                return self._success_result(posted_url="https://alpha.com/post/100", public_access=True)

        class MockFailingPlatform(BasePlatform):
            @property
            def platform_name(self) -> str:
                return "Platform Beta (Failure)"

            def is_configured(self) -> bool:
                return True

            async def _execute_post(self, message, cta_url, client) -> PlatformResult:
                return self._failure_result("Authentication failed")

            def _generate_mock_result(self, message, cta_url) -> PlatformResult:
                return self._failure_result("Authentication failed")

        mock_service = PostingService(platforms=[MockSuccessPlatform(), MockFailingPlatform()])
        monkeypatch.setattr(client.app.state, "posting_service", mock_service)

        payload = {"message": "Great news at https://example.com"}
        response = client.post("/posting", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert len(data["results"]) == 2

        alpha = next(r for r in data["results"] if r["platform"] == "Platform Alpha (Success)")
        beta = next(r for r in data["results"] if r["platform"] == "Platform Beta (Failure)")

        assert alpha["status"] == "success"
        assert alpha["posted_url"] == "https://alpha.com/post/100"
        assert alpha["public_access"] is True
        assert alpha["error"] is None

        assert beta["status"] == "failed"
        assert beta["posted_url"] is None
        assert beta["public_access"] is False
        assert beta["error"] == "Authentication failed"
