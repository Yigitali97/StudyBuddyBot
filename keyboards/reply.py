"""
Keyboard utilities for StudyBuddy Telegram Bot.

This module provides inline and reply keyboards for interactive bot conversations.
"""

import logging
from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

logger = logging.getLogger(__name__)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Create the main menu keyboard with command buttons.

    Returns:
        ReplyKeyboardMarkup with main menu buttons.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Add Task"), KeyboardButton(text="📋 List Tasks")],
            [KeyboardButton(text="🗑️ Delete Task"), KeyboardButton(text="❓ Help")],
        ],
        resize_keyboard=True,
        persistent=True,
        input_field_placeholder="Choose an option or type a command...",
    )
    return keyboard


def get_task_type_keyboard() -> InlineKeyboardMarkup:
    """
    Get inline keyboard for task type selection.

    Returns:
        InlineKeyboardMarkup with Assignment and Exam options.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Assignment", callback_data="type_assignment"
                ),
                InlineKeyboardButton(text="📖 Exam", callback_data="type_exam"),
            ]
        ]
    )
    return keyboard


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Get inline keyboard for confirmation (Yes/No).

    Returns:
        InlineKeyboardMarkup with Yes and No buttons.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yes", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ No", callback_data="confirm_no"),
            ]
        ]
    )
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Get reply keyboard with cancel button.

    Returns:
        ReplyKeyboardMarkup with Cancel button.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Cancel")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return keyboard


def remove_keyboard() -> ReplyKeyboardRemove:
    """
    Get keyboard removal object.

    Returns:
        ReplyKeyboardRemove to hide custom keyboard.
    """
    return ReplyKeyboardRemove()


def get_task_selection_keyboard(
    task_ids: List[int], task_titles: List[str], max_per_row: int = 2
) -> InlineKeyboardMarkup:
    """
    Get inline keyboard for task selection.

    Args:
        task_ids: List of task IDs.
        task_titles: List of task titles (truncated).
        max_per_row: Maximum number of buttons per row.

    Returns:
        InlineKeyboardMarkup with task selection buttons.
    """
    buttons = []

    for i, (task_id, title) in enumerate(zip(task_ids, task_titles)):
        # Truncate title if too long
        display_title = title if len(title) <= 30 else title[:27] + "..."
        button = InlineKeyboardButton(
            text=f"{i + 1}. {display_title}", callback_data=f"task_{task_id}"
        )

        # Add button to current row or create new row
        if i % max_per_row == 0:
            buttons.append([button])
        else:
            buttons[-1].append(button)

    # Add cancel button at the end
    buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_numbered_keyboard(count: int, prefix: str = "num") -> InlineKeyboardMarkup:
    """
    Get inline keyboard with numbered buttons.

    Args:
        count: Number of buttons to create.
        prefix: Callback data prefix.

    Returns:
        InlineKeyboardMarkup with numbered buttons.
    """
    buttons = []
    row = []

    for i in range(1, count + 1):
        button = InlineKeyboardButton(text=str(i), callback_data=f"{prefix}_{i}")
        row.append(button)

        # Create new row after every 5 buttons
        if i % 5 == 0:
            buttons.append(row)
            row = []

    # Add remaining buttons
    if row:
        buttons.append(row)

    # Add cancel button
    buttons.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
