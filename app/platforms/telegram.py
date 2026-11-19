"""
Telegram Bot API integration adapter.
"""
import uuid
import httpx

from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult


class TelegramPlatform(BasePlatform):
    """Posts messages to a Telegram Channel or Group via Telegram Bot API."""

    @property
    def platform_name(self) -> str:
        return "Telegram"

    def is_configured(self) -> bool:
        return bool(settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID)

    async def _execute_post(self, message: str, cta_url: str, client: httpx.AsyncClient) -> PlatformResult:
        api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "disable_web_page_preview": False,
        }

        response = await client.post(
            api_url,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            return self._failure_result(f"Telegram API error: {data.get('description', 'Unknown error')}")

        result = data.get("result", {})
        message_id = result.get("message_id")
        chat = result.get("chat", {})
        username = chat.get("username")

        if username:
            posted_url = f"https://t.me/{username}/{message_id}"
        else:
            chat_id = str(chat.get("id", settings.TELEGRAM_CHAT_ID)).replace("-100", "").replace("-", "")
            posted_url = f"https://t.me/c/{chat_id}/{message_id}"

        return self._success_result(posted_url=posted_url, public_access=True)

    def _generate_mock_result(self, message: str, cta_url: str) -> PlatformResult:
        mock_id = (abs(hash(message)) % 9000) + 1000
        return self._success_result(
            posted_url=f"https://t.me/tech_announcements/{mock_id}",
            public_access=True,
        )
