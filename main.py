"""
StudyBuddy Telegram Bot - Main Entry Point

This is the main application file that initializes and runs the bot.
It sets up all handlers, services, and starts polling for updates.
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import Config
from database.db import db
from handlers import add, delete, help, list, start
from services.reminder import initialize_reminder_service

# Setup logging
logger = Config.setup_logging()


async def set_bot_commands(bot: Bot):
    """
    Set bot commands menu for Telegram.

    This makes commands appear in the Telegram menu when users type '/'.
    """
    commands = [
        BotCommand(command="start", description="🚀 Start the bot"),
        BotCommand(command="add", description="➕ Add a new task"),
        BotCommand(command="list", description="📋 View all tasks"),
        BotCommand(command="delete", description="🗑️ Delete a task"),
        BotCommand(command="help", description="❓ Get help"),
        BotCommand(command="cancel", description="❌ Cancel current action"),
    ]

    await bot.set_my_commands(commands)
    logger.info("Bot commands menu set successfully")


async def on_startup():
    """
    Execute actions on bot startup.

    Initializes the database and starts background services.
    """
    logger.info("Bot is starting up...")

    # Initialize database
    try:
        await db.initialize()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise

    logger.info("Startup complete!")


async def on_shutdown():
    """
    Execute actions on bot shutdown.

    Closes database connections and stops background services.
    """
    logger.info("Bot is shutting down...")

    # Close database connection
    try:
        await db.disconnect()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}", exc_info=True)

    logger.info("Shutdown complete!")


async def main():
    """
    Main function to run the bot.

    Sets up the bot, dispatcher, handlers, and starts polling.
    """
    try:
        # Validate configuration
        Config.validate()

        # Create bot instance
        bot = Bot(
            token=Config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        # Create dispatcher with FSM storage
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Register handlers
        # Order matters: more specific handlers should be registered first
        dp.include_router(start.router)
        dp.include_router(help.router)
        dp.include_router(add.router)
        dp.include_router(list.router)
        dp.include_router(delete.router)

        logger.info("All handlers registered")

        # Initialize and start reminder service
        reminder_service = initialize_reminder_service(bot)
        reminder_service.start()

        # Run startup actions
        await on_startup()

        # Set bot commands menu
        await set_bot_commands(bot)

        # Log bot info
        bot_info = await bot.get_me()
        logger.info(f"Bot started: @{bot_info.username}")
        logger.info(f"Bot ID: {bot_info.id}")
        logger.info(f"Bot name: {bot_info.first_name}")

        # Start polling
        logger.info("Starting polling...")

        try:
            await dp.start_polling(
                bot,
                allowed_updates=dp.resolve_used_update_types(),
                drop_pending_updates=True,  # Skip old updates on restart
            )
        finally:
            # Stop reminder service
            reminder_service.stop()

            # Run shutdown actions
            await on_shutdown()

            # Close bot session
            await bot.session.close()

    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        # Run the bot
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
