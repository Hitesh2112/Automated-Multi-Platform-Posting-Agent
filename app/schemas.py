"""
Pydantic schemas for request validation and standardized response formatting.
"""
import re
from typing import List, Literal, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Regex to detect HTTP/HTTPS URLs and www. links in message text
URL_REGEX = re.compile(r'(?:https?://|www\.)[^\s<>"]+', re.IGNORECASE)

# Trailing punctuation that might stick to a URL at the end of a sentence
TRAILING_PUNCTUATION = ".,!?;:)]\"'"


class PostingRequest(BaseModel):
    """Request model for the POST /posting endpoint."""

    message: str = Field(
        ...,
        description="Short message with exactly one CTA link, maximum 200 characters.",
        examples=["Check out our latest business platform and grow your online visibility. https://example.com"],
    )

    # Cached CTA URL after validation
    _extracted_url: str = ""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "message": "Check out our latest business platform and grow your online visibility. https://example.com"
            }
        },
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, raw_msg: str) -> str:
        # 1. Clean and check non-empty
        cleaned_msg = raw_msg.strip()
        if not cleaned_msg:
            raise ValueError("Message cannot be empty.")

        # 2. Character length constraint (max 200 characters)
        if len(cleaned_msg) > 200:
            raise ValueError(
                f"Message must not exceed 200 characters (current length: {len(cleaned_msg)})."
            )

        # 3. Extract candidate URLs
        matches = URL_REGEX.findall(cleaned_msg)
        cleaned_urls = [m.rstrip(TRAILING_PUNCTUATION) for m in matches]

        # 4. Enforce exactly one CTA link
        if len(cleaned_urls) == 0:
            raise ValueError("Message must contain exactly one CTA link, found 0.")
        if len(cleaned_urls) > 1:
            raise ValueError(
                f"Message must contain exactly one CTA link, found {len(cleaned_urls)}: {cleaned_urls}."
            )

        url = cleaned_urls[0]

        # Normalize www. to https://www. if missing scheme
        if url.lower().startswith("www."):
            url = f"https://{url}"

        # 5. Validate URL structure
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid URL scheme '{parsed.scheme}': must be http or https.")

        netloc = parsed.netloc.strip()
        if not netloc or "." not in netloc:
            raise ValueError(f"Invalid domain in URL: '{url}'.")

        return cleaned_msg

    @property
    def cta_url(self) -> str:
        """Extract and return the single validated CTA URL."""
        matches = URL_REGEX.findall(self.message)
        if matches:
            url = matches[0].rstrip(TRAILING_PUNCTUATION)
            if url.lower().startswith("www."):
                return f"https://{url}"
            return url
        return ""


class PlatformResult(BaseModel):
    """Posting result for an individual platform."""

    platform: str = Field(description="Platform name (e.g. Telegram, Twitter / X)")
    status: Literal["success", "failed"] = Field(description="Execution status")
    posted_url: Optional[str] = Field(default=None, description="Published content URL, if successful")
    public_access: bool = Field(default=False, description="Whether the published content is publicly accessible")
    date: Optional[str] = Field(default=None, description="Posting date in YYYY-MM-DD format")
    time: Optional[str] = Field(default=None, description="Posting time in HH:MM:SS format")
    error: Optional[str] = Field(default=None, description="Error details, if failed")


class PostingResponse(BaseModel):
    """Aggregate response returned by the /posting endpoint."""

    success: bool = Field(description="Whether at least one platform succeeded or all succeeded")
    results: List[PlatformResult] = Field(description="List of individual platform posting results")
