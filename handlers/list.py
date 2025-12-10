"""
List command handler for StudyBuddy Telegram Bot.

This module handles the /list command, which displays all upcoming
tasks for the user.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from database.models import Task, User
from keyboards.reply import get_main_menu_keyboard
from utils.formatters import format_task_list

logger = logging.getLogger(__name__)

# Create router for list command
router = Router()


@router.message(F.text == "📋 List Tasks")
@router.message(Command("list"))
async def cmd_list(message: Message):
    """
    Handle /list command.

    Displays all upcoming tasks for the user, sorted by due date.

    Args:
        message: Incoming message object.
    """
    user_id = message.from_user.id

    # Update user's last_active timestamp
    await User.create_or_update(user_id=user_id)

    logger.info(f"User {user_id} requested task list")

    # Get all upcoming tasks for the user
    tasks = await Task.get_user_tasks(user_id=user_id, include_past=False)

    # Format and send the task list
    task_list_message = format_task_list(tasks)

    await message.answer(task_list_message, reply_markup=get_main_menu_keyboard())

    # Log task count
    logger.info(f"Displayed {len(tasks)} tasks for user {user_id}")
