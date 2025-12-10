"""
Reminder service for StudyBuddy Telegram Bot.

This module provides background job scheduling for automated task reminders.
Checks for tasks due in 24 hours and sends reminder notifications to users.
"""

import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import Config
from database.models import Task
from utils.formatters import format_reminder_message

logger = logging.getLogger(__name__)


class ReminderService:
    """Service for managing automated task reminders."""

    def __init__(self, bot: Bot):
        """
        Initialize reminder service.

        Args:
            bot: Aiogram Bot instance for sending messages.
        """
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        logger.info("Reminder service initialized")

    async def check_and_send_reminders(self):
        """
        Check for tasks needing reminders and send notifications.

        This method is called periodically by the scheduler.
        It finds all tasks due in 24-25 hours that haven't been reminded yet,
        sends reminder messages, and marks them as reminded.
        """
        try:
            logger.info("Running reminder check...")

            # Get tasks that need reminders
            tasks = await Task.get_tasks_needing_reminder()

            if not tasks:
                logger.info("No tasks need reminders at this time")
                return

            logger.info(f"Found {len(tasks)} task(s) needing reminders")

            # Send reminder for each task
            reminders_sent = 0
            reminders_failed = 0

            for task in tasks:
                try:
                    user_id = task["user_id"]
                    task_id = task["id"]

                    # Format reminder message
                    reminder_message = format_reminder_message(task)

                    # Send reminder to user
                    await self.bot.send_message(chat_id=user_id, text=reminder_message)

                    # Mark task as reminded
                    await Task.mark_as_reminded(task_id)

                    reminders_sent += 1
                    logger.info(
                        f"Sent reminder for task {task_id} to user {user_id}: {task['title']}"
                    )

                except Exception as e:
                    reminders_failed += 1
                    logger.error(
                        f"Failed to send reminder for task {task.get('id')}: {e}",
                        exc_info=True,
                    )

            logger.info(
                f"Reminder check complete. Sent: {reminders_sent}, Failed: {reminders_failed}"
            )

        except Exception as e:
            logger.error(f"Error in reminder check: {e}", exc_info=True)

    def start(self):
        """
        Start the reminder scheduler.

        Sets up a periodic job that runs every N minutes (configured in settings)
        to check for tasks needing reminders.
        """
        if self.is_running:
            logger.warning("Reminder service is already running")
            return

        # Add periodic job
        interval_minutes = Config.REMINDER_INTERVAL_MINUTES

        self.scheduler.add_job(
            self.check_and_send_reminders,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id="reminder_check",
            name="Check and send task reminders",
            replace_existing=True,
            max_instances=1,  # Prevent overlapping runs
        )

        # Start the scheduler
        self.scheduler.start()
        self.is_running = True

        logger.info(
            f"Reminder service started. Checking every {interval_minutes} minute(s)"
        )

        # Run initial check immediately
        asyncio.create_task(self.check_and_send_reminders())

    def stop(self):
        """
        Stop the reminder scheduler.

        Gracefully shuts down the scheduler and waits for any running jobs to complete.
        """
        if not self.is_running:
            logger.warning("Reminder service is not running")
            return

        self.scheduler.shutdown(wait=True)
        self.is_running = False

        logger.info("Reminder service stopped")

    async def send_test_reminder(self, user_id: int, task_id: int):
        """
        Send a test reminder for a specific task (for testing purposes).

        Args:
            user_id: User ID to send reminder to.
            task_id: Task ID to send reminder for.

        Returns:
            True if reminder was sent successfully, False otherwise.
        """
        try:
            task = await Task.get_by_id(task_id)

            if not task:
                logger.warning(f"Task {task_id} not found for test reminder")
                return False

            if task["user_id"] != user_id:
                logger.warning(f"Task {task_id} does not belong to user {user_id}")
                return False

            # Format and send reminder
            reminder_message = format_reminder_message(task)
            await self.bot.send_message(chat_id=user_id, text=reminder_message)

            logger.info(f"Sent test reminder for task {task_id} to user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send test reminder: {e}", exc_info=True)
            return False

    def get_status(self) -> dict:
        """
        Get current status of the reminder service.

        Returns:
            Dictionary with service status information.
        """
        return {
            "is_running": self.is_running,
            "interval_minutes": Config.REMINDER_INTERVAL_MINUTES,
            "next_run": (
                self.scheduler.get_job("reminder_check").next_run_time
                if self.is_running
                else None
            ),
        }


# Singleton instance (will be initialized in main.py)
reminder_service: ReminderService = None


def get_reminder_service() -> ReminderService:
    """
    Get the global reminder service instance.

    Returns:
        ReminderService instance.

    Raises:
        RuntimeError: If reminder service hasn't been initialized.
    """
    if reminder_service is None:
        raise RuntimeError(
            "Reminder service not initialized. Call initialize_reminder_service() first."
        )
    return reminder_service


def initialize_reminder_service(bot: Bot) -> ReminderService:
    """
    Initialize the global reminder service instance.

    Args:
        bot: Aiogram Bot instance.

    Returns:
        Initialized ReminderService instance.
    """
    global reminder_service
    reminder_service = ReminderService(bot)
    return reminder_service
