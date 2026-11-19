"""
Platform adapters package.
"""
from app.platforms.base import BasePlatform
from app.platforms.registry import get_all_platforms

__all__ = ["BasePlatform", "get_all_platforms"]
