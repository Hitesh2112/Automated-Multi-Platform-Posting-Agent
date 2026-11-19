"""
Custom exception hierarchy and error schemas.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Specific field or issue detail."""
    field: Optional[str] = Field(default=None, description="The field that triggered the error")
    issue: str = Field(description="Description of the specific problem")


class ErrorContainer(BaseModel):
    """Structured error payload container."""
    code: str = Field(description="Standardized error code (e.g. VALIDATION_ERROR)")
    message: str = Field(description="Human-readable error summary")
    details: Optional[List[ErrorDetail]] = Field(default=None, description="Detailed list of specific errors")


class ErrorResponse(BaseModel):
    """Top-level error response model."""
    success: bool = Field(default=False, description="Always false for error responses")
    error: ErrorContainer = Field(description="Error body details")


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[List[Dict[str, Any]]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or []


class ValidationException(AppException):
    """Raised when request payload or business rules fail validation."""

    def __init__(self, message: str, details: Optional[List[Dict[str, Any]]] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details or [],
        )


class PlatformException(Exception):
    """Base exception for third-party platform integration failures."""

    def __init__(self, platform: str, message: str, status_code: Optional[int] = None):
        super().__init__(f"[{platform}] {message}")
        self.platform = platform
        self.message = message
        self.status_code = status_code


class PlatformAuthException(PlatformException):
    """Raised when authentication credentials are missing or rejected."""

    def __init__(self, platform: str, message: str = "Authentication failed"):
        super().__init__(platform=platform, message=message, status_code=401)


class PlatformNetworkException(PlatformException):
    """Raised when a network timeout or connection error occurs."""

    def __init__(self, platform: str, message: str = "Network request failed or timed out"):
        super().__init__(platform=platform, message=message, status_code=504)


class PlatformRateLimitException(PlatformException):
    """Raised when a platform rate limits the request."""

    def __init__(self, platform: str, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        super().__init__(platform=platform, message=message, status_code=429)
        self.retry_after = retry_after


class PlatformApiException(PlatformException):
    """Raised when remote platform returns an unexpected HTTP error."""

    def __init__(self, platform: str, status_code: int, response_body: str):
        super().__init__(
            platform=platform,
            message=f"API error (HTTP {status_code}): {response_body}",
            status_code=status_code,
        )
