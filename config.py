"""
Configuration management for StudyBuddy Telegram Bot.

This module loads and validates environment variables and provides
a central configuration object for the application.
"""

import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""

    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///studybuddy.db")

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # Reminder Configuration
    REMINDER_INTERVAL_MINUTES = int(os.getenv("REMINDER_INTERVAL_MINUTES", "60"))

    # Timezone Configuration
    TIMEZONE = os.getenv("TIMEZONE", "UTC")

    # Conversation timeout (in seconds)
    CONVERSATION_TIMEOUT = 120  # 2 minutes

    # Maximum task title length
    MAX_TASK_TITLE_LENGTH = 200

    # Maximum tasks to display per page
    MAX_TASKS_PER_PAGE = 50

    @classmethod
    def validate(cls):
        """
        Validate that all required configuration values are set.

        Raises:
            ValueError: If required configuration is missing.
        """
        if not cls.BOT_TOKEN:
            raise ValueError(
                "BOT_TOKEN is not set. Please create a .env file with your "
                "Telegram bot token. See .env.example for reference."
            )

        if cls.REMINDER_INTERVAL_MINUTES < 1:
            raise ValueError("REMINDER_INTERVAL_MINUTES must be at least 1 minute.")

        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {', '.join(valid_log_levels)}")

    @classmethod
    def setup_logging(cls):
        """Configure application logging."""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Set aiogram logging level
        logging.getLogger("aiogram").setLevel(logging.INFO)

        logger = logging.getLogger(__name__)
        logger.info(f"Logging configured with level: {cls.LOG_LEVEL}")

        return logger


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    raise
