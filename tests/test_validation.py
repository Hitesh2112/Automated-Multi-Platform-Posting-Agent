"""
Unit tests for message input validation and URL constraints.
"""
import pytest
from pydantic import ValidationError

from app.schemas import PostingRequest


class TestInputValidation:
    """Test suite covering the 200 character limit, single CTA link, and URL validity."""

    def test_valid_message_with_https_url(self):
        msg = "Check out our latest business platform and grow your online visibility. https://example.com"
        req = PostingRequest(message=msg)
        assert req.message == msg
        assert req.cta_url == "https://example.com"

    def test_valid_message_with_http_url(self):
        msg = "Visit our documentation portal here: http://docs.example.org"
        req = PostingRequest(message=msg)
        assert req.cta_url == "http://docs.example.org"

    def test_valid_message_with_www_prefix(self):
        msg = "Find the latest updates on www.myservice.io now!"
        req = PostingRequest(message=msg)
        assert req.cta_url == "https://www.myservice.io"

    def test_valid_message_exactly_200_chars(self):
        url = "https://example.com"
        prefix = "A" * (200 - len(url) - 1)
        msg = f"{prefix} {url}"
        assert len(msg) == 200
        req = PostingRequest(message=msg)
        assert req.cta_url == url

    def test_message_exceeding_200_chars_fails(self):
        url = "https://example.com"
        prefix = "A" * (201 - len(url) - 1)
        msg = f"{prefix} {url}"
        assert len(msg) == 201
        with pytest.raises(ValidationError) as exc_info:
            PostingRequest(message=msg)
        assert "Message must not exceed 200 characters" in str(exc_info.value)

    def test_message_with_no_cta_link_fails(self):
        msg = "Welcome to our brand new platform! Try out all features."
        with pytest.raises(ValidationError) as exc_info:
            PostingRequest(message=msg)
        assert "Message must contain exactly one CTA link, found 0" in str(exc_info.value)

    def test_message_with_multiple_cta_links_fails(self):
        msg = "Visit https://first.com and also check https://second.com for info"
        with pytest.raises(ValidationError) as exc_info:
            PostingRequest(message=msg)
        assert "Message must contain exactly one CTA link, found 2" in str(exc_info.value)

    def test_message_with_three_cta_links_fails(self):
        msg = "Link 1: https://a.com Link 2: https://b.com Link 3: https://c.com"
        with pytest.raises(ValidationError) as exc_info:
            PostingRequest(message=msg)
        assert "Message must contain exactly one CTA link, found 3" in str(exc_info.value)

    def test_empty_message_fails(self):
        with pytest.raises(ValidationError) as exc_info:
            PostingRequest(message="   ")
        assert "Message cannot be empty" in str(exc_info.value)

    def test_url_with_trailing_punctuation_is_cleaned(self):
        msg = "Check our platform at https://example.com/demo. You will love it!"
        req = PostingRequest(message=msg)
        assert req.cta_url == "https://example.com/demo"
