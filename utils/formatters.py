"""
Message formatting utilities for StudyBuddy Telegram Bot.

This module provides functions for formatting messages, dates, and task lists
in a user-friendly way.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def format_date(task_date: date) -> str:
    """
    Format a date in a user-friendly way.

    Args:
        task_date: Date to format.

    Returns:
        Formatted date string (e.g., "December 15, 2025").
    """
    return task_date.strftime("%B %d, %Y")


def format_relative_time(task_date: date) -> str:
    """
    Format date as relative time (e.g., "in 3 days", "tomorrow", "today").

    Args:
        task_date: Date to format.

    Returns:
        Relative time string.
    """
    today = date.today()
    delta = (task_date - today).days

    if delta < 0:
        return "overdue"
    elif delta == 0:
        return "today"
    elif delta == 1:
        return "tomorrow"
    elif delta < 7:
        return f"in {delta} days"
    elif delta < 14:
        return "in 1 week"
    elif delta < 30:
        weeks = delta // 7
        return f"in {weeks} weeks"
    elif delta < 60:
        return "in 1 month"
    else:
        months = delta // 30
        return f"in {months} months"


def get_task_icon(task_type: str) -> str:
    """
    Get emoji icon for task type.

    Args:
        task_type: Type of task ('assignment' or 'exam').

    Returns:
        Emoji icon string.
    """
    if task_type.lower() == "assignment":
        return "📝"
    elif task_type.lower() == "exam":
        return "📖"
    else:
        return "📌"


def format_task_summary(task: Dict[str, Any]) -> str:
    """
    Format a single task as a summary line.

    Args:
        task: Task dictionary from database.

    Returns:
        Formatted task summary string.
    """
    icon = get_task_icon(task["task_type"])
    title = task["title"]

    # Parse due_date (it's stored as ISO string in SQLite)
    if isinstance(task["due_date"], str):
        task_date = date.fromisoformat(task["due_date"])
    else:
        task_date = task["due_date"]

    relative = format_relative_time(task_date)
    date_str = format_date(task_date)

    return f"{icon} {title}\n   Due: {date_str} ({relative})"


def format_task_list(tasks: List[Dict[str, Any]]) -> str:
    """
    Format a list of tasks for display.

    Args:
        tasks: List of task dictionaries.

    Returns:
        Formatted task list string.
    """
    if not tasks:
        return "🎉 No upcoming tasks!\n\nUse /add to create a new task."

    message_parts = ["📋 Your Upcoming Tasks:\n"]

    for index, task in enumerate(tasks, start=1):
        task_summary = format_task_summary(task)
        message_parts.append(f"\n{index}. {task_summary}")

    return "\n".join(message_parts)


def format_task_details(task: Dict[str, Any]) -> str:
    """
    Format complete task details for confirmation or deletion.

    Args:
        task: Task dictionary from database.

    Returns:
        Formatted task details string.
    """
    icon = get_task_icon(task["task_type"])
    title = task["title"]

    # Parse due_date
    if isinstance(task["due_date"], str):
        task_date = date.fromisoformat(task["due_date"])
    else:
        task_date = task["due_date"]

    date_str = format_date(task_date)
    task_type_display = task["task_type"].capitalize()

    return f"{icon} {title}\n📅 Due: {date_str}\n📚 Type: {task_type_display}"


def format_reminder_message(task: Dict[str, Any]) -> str:
    """
    Format a reminder message for a task.

    Args:
        task: Task dictionary from database.

    Returns:
        Formatted reminder message.
    """
    icon = get_task_icon(task["task_type"])
    title = task["title"]

    # Parse due_date
    if isinstance(task["due_date"], str):
        task_date = date.fromisoformat(task["due_date"])
    else:
        task_date = task["due_date"]

    date_str = format_date(task_date)
    day_name = task_date.strftime("%A")  # e.g., "Monday"

    return (
        f"⏰ REMINDER\n\n"
        f"{icon} {title}\n"
        f"📅 Due: Tomorrow, {day_name} ({date_str})\n\n"
        f"Don't forget! 📚"
    )


def format_task_confirmation(task_type: str, title: str, due_date: date) -> str:
    """
    Format task creation confirmation message.

    Args:
        task_type: Type of task ('assignment' or 'exam').
        title: Task title.
        due_date: Task due date.

    Returns:
        Formatted confirmation message.
    """
    icon = get_task_icon(task_type)
    date_str = format_date(due_date)

    # Calculate reminder date
    reminder_date = due_date - timedelta(days=1)
    reminder_str = format_date(reminder_date)

    return (
        f"✅ Task Added Successfully!\n\n"
        f"{icon} {title}\n"
        f"📅 Due: {date_str}\n"
        f"⏰ Reminder: {reminder_str} (24 hours before)"
    )


def format_deletion_confirmation(task: Dict[str, Any]) -> str:
    """
    Format task deletion confirmation prompt.

    Args:
        task: Task dictionary from database.

    Returns:
        Formatted confirmation prompt.
    """
    task_details = format_task_details(task)

    return (
        f"Are you sure you want to delete this task?\n\n"
        f"{task_details}\n\n"
        f"Reply with YES to confirm or NO to cancel."
    )


def format_task_selection_list(tasks: List[Dict[str, Any]]) -> str:
    """
    Format a numbered list of tasks for selection.

    Args:
        tasks: List of task dictionaries.

    Returns:
        Formatted selection list.
    """
    if not tasks:
        return "You have no tasks to select from."

    message_parts = ["Select a task:\n"]

    for index, task in enumerate(tasks, start=1):
        icon = get_task_icon(task["task_type"])
        title = task["title"]

        # Parse due_date
        if isinstance(task["due_date"], str):
            task_date = date.fromisoformat(task["due_date"])
        else:
            task_date = task["due_date"]

        # Short date format for selection
        date_str = task_date.strftime("%b %d")

        message_parts.append(f"{index}. {icon} {title} ({date_str})")

    return "\n".join(message_parts)


def escape_markdown(text: str) -> str:
    """
    Escape special characters for Telegram Markdown.

    Args:
        text: Text to escape.

    Returns:
        Escaped text.
    """
    # Characters that need to be escaped in Telegram MarkdownV2
    special_chars = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]

    for char in special_chars:
        text = text.replace(char, f"\\{char}")

    return text


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to maximum length with ellipsis.

    Args:
        text: Text to truncate.
        max_length: Maximum length.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."
