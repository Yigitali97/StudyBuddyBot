"""
Database package for StudyBuddy Telegram Bot.

This package provides database connectivity and models for the application.
"""

from database.db import Database, db
from database.models import Task, User

__all__ = ["Database", "db", "User", "Task"]
