"""
Unit tests for custom exception handlers and standardized error responses.
"""
from fastapi.testclient import TestClient


class TestErrorHandlers:
    """Verify custom error structures and HTTP status codes."""

    def test_validation_error_missing_body(self, client: TestClient):
        response = client.post("/posting", json={})
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert "details" in data["error"]
        assert any(d["field"] == "message" for d in data["error"]["details"])

    def test_validation_error_over_200_chars(self, client: TestClient):
        long_text = "X" * 205 + " https://example.com"
        response = client.post("/posting", json={"message": long_text})
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "VALIDATION_ERROR"
        details = data["error"]["details"]
        assert any("exceed 200 characters" in d["issue"] for d in details)

    def test_validation_error_no_urls(self, client: TestClient):
        response = client.post("/posting", json={"message": "No link included here"})
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        details = data["error"]["details"]
        assert any("found 0" in d["issue"] for d in details)

    def test_health_check_endpoint(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "platforms_count" in data
        assert data["platforms_count"] >= 5
