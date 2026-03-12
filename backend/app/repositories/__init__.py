"""
Repository layer for FitCoach AI.

Provides data access abstraction for all database operations.
"""

from .base_repository import BaseRepository
from .user_repository import UserRepository
from .profile_repository import ProfileRepository
from .goal_repository import GoalRepository
from .progress_repository import ProgressRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "ProfileRepository",
    "GoalRepository",
    "ProgressRepository",
]
