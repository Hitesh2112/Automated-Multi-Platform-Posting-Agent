"""
Platform registry for discovering and managing active platform adapters.
"""
from typing import List

from app.platforms.base import BasePlatform
from app.platforms.github import GitHubPlatform
from app.platforms.instagram_threads import InstagramThreadsPlatform
from app.platforms.linkedin import LinkedInPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.twitter import TwitterPlatform


def get_all_platforms() -> List[BasePlatform]:
    """
    Return instances of all registered platform adapters.
    Add or remove platforms here without touching the core posting service.
    """
    return [
        TelegramPlatform(),
        TwitterPlatform(),
        LinkedInPlatform(),
        RedditPlatform(),
        GitHubPlatform(),
        InstagramThreadsPlatform(),
    ]
