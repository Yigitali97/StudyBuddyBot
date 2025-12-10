"""
Help command handler for StudyBuddy Telegram Bot.

This module handles the /help command, which displays all available
commands and usage instructions.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from database.models import User
from keyboards.reply import get_main_menu_keyboard

logger = logging.getLogger(__name__)

# Create router for help command
router = Router()


@router.message(F.text == "❓ Help")
@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Handle /help command.

    Displays all available commands with descriptions and usage examples.

    Args:
        message: Incoming message object.
    """
    user_id = message.from_user.id

    # Update user's last_active timestamp
    await User.create_or_update(user_id=user_id)

    logger.info(f"User {user_id} requested help")

    help_message = (
        "📚 <b>StudyBuddy Help</b>\n\n"
        "<b>Available Commands:</b>\n\n"
        "🚀 /start - Start the bot and see welcome message\n"
        "➕ Add Task - Create a new assignment or exam\n"
        "📋 List Tasks - View all upcoming tasks\n"
        "🗑️ Delete Task - Remove a completed task\n"
        "❓ Help - Show this help message\n\n"
        "<b>💡 Tips:</b>\n"
        "• Dates must be in DD/MM/YYYY format (e.g., 25/12/2025)\n"
        "• You'll receive reminders 24 hours before deadlines\n"
        "• Use /list to check what's coming up\n"
        "• Task titles can be up to 200 characters long\n\n"
        "<b>📝 How to Add a Task:</b>\n"
        "1. Send /add command\n"
        "2. Choose task type (Assignment or Exam)\n"
        "3. Enter task name\n"
        "4. Enter due date in DD/MM/YYYY format\n"
        "5. Get automatic reminder 24 hours before!\n\n"
        "<b>🔔 Reminder System:</b>\n"
        "You'll automatically receive a reminder 24 hours before "
        "each task is due. No need to worry about forgetting!\n\n"
        "<b>Questions or issues?</b>\n"
        "Contact the developer or check the documentation."
    )

    await message.answer(
        help_message, parse_mode="HTML", reply_markup=get_main_menu_keyboard()
    )
