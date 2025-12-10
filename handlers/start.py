"""
Start command handler for StudyBuddy Telegram Bot.

This module handles the /start command, which greets users and
registers them in the database.
"""

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.models import User
from keyboards.reply import get_main_menu_keyboard

logger = logging.getLogger(__name__)

# Create router for start command
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handle /start command.

    Greets the user and creates/updates their record in the database.

    Args:
        message: Incoming message object.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Student"

    # Create or update user in database
    await User.create_or_update(
        user_id=user_id, username=username, first_name=first_name
    )

    logger.info(f"User {user_id} ({first_name}) started the bot")

    welcome_message = (
        f"👋 Welcome to StudyBuddy, {first_name}!\n\n"
        f"I help you manage assignments and exam deadlines "
        f"so you never miss important dates.\n\n"
        f"🚀 Quick Start:\n"
        f"Use the buttons below to get started!\n\n"
        f"• ➕ Add Task - Create a new assignment or exam\n"
        f"• 📋 List Tasks - View all upcoming deadlines\n"
        f"• 🗑️ Delete Task - Remove completed tasks\n"
        f"• ❓ Help - Get detailed help\n\n"
        f"Let's ace those deadlines! 📚✨"
    )

    await message.answer(welcome_message, reply_markup=get_main_menu_keyboard())
