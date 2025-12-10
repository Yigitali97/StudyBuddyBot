"""
Validation utilities for StudyBuddy Telegram Bot.

This module provides functions for validating user input,
including date formats and task titles.
"""

import logging
import re
from datetime import date, datetime
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def validate_date(date_string: str) -> Tuple[bool, Optional[date], Optional[str]]:
    """
    Validate and parse a date string.

    Accepts formats: DD/MM/YYYY or DD.MM.YYYY

    Args:
        date_string: Date string to validate.

    Returns:
        Tuple of (is_valid, parsed_date, error_message)
        - is_valid: True if date is valid and in the future
        - parsed_date: datetime.date object if valid, None otherwise
        - error_message: Error message if invalid, None if valid
    """
    date_string = date_string.strip()

    # Try different date formats
    formats = [
        "%d/%m/%Y",  # DD/MM/YYYY
        "%d.%m.%Y",  # DD.MM.YYYY
        "%d-%m-%Y",  # DD-MM-YYYY
    ]

    parsed_date = None

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(date_string, date_format).date()
            break
        except ValueError:
            continue

    if parsed_date is None:
        return (
            False,
            None,
            "❌ Invalid date format. Please use DD/MM/YYYY (e.g., 25/12/2025)",
        )

    # Check if date is in the future
    today = date.today()
    if parsed_date < today:
        return (
            False,
            None,
            "❌ Date must be in the future. Please enter a valid due date.",
        )

    # Check if date is too far in the future (more than 2 years)
    max_date = date(today.year + 2, today.month, today.day)
    if parsed_date > max_date:
        return (
            False,
            None,
            "❌ Date is too far in the future (max 2 years). Please check the date.",
        )

    return True, parsed_date, None


def validate_task_title(
    title: str, max_length: int = 200
) -> Tuple[bool, str, Optional[str]]:
    """
    Validate task title.

    Args:
        title: Task title to validate.
        max_length: Maximum allowed length for title.

    Returns:
        Tuple of (is_valid, sanitized_title, error_message)
        - is_valid: True if title is valid
        - sanitized_title: Cleaned title string
        - error_message: Error message if invalid, None if valid
    """
    # Remove leading/trailing whitespace
    title = title.strip()

    # Check if empty
    if not title:
        return False, "", "❌ Task title cannot be empty. Please enter a valid title."

    # Check length
    if len(title) > max_length:
        return (
            False,
            title,
            f"❌ Task title is too long (max {max_length} characters). "
            f"Your title has {len(title)} characters.",
        )

    # Check for minimum length
    if len(title) < 3:
        return (
            False,
            title,
            "❌ Task title is too short (min 3 characters). Please be more descriptive.",
        )

    # Sanitize: remove multiple consecutive spaces
    title = re.sub(r"\s+", " ", title)

    return True, title, None


def validate_task_type(task_type: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate task type selection.

    Args:
        task_type: Task type string from user.

    Returns:
        Tuple of (is_valid, normalized_type, error_message)
        - is_valid: True if type is valid
        - normalized_type: Normalized type ('assignment' or 'exam')
        - error_message: Error message if invalid, None if valid
    """
    task_type = task_type.strip().lower()

    # Accept various formats
    if task_type in ["1", "assignment", "assign", "hw", "homework"]:
        return True, "assignment", None
    elif task_type in ["2", "exam", "test", "quiz", "midterm", "final"]:
        return True, "exam", None
    else:
        return (
            False,
            None,
            "❌ Invalid task type. Please select:\n1️⃣ Assignment\n2️⃣ Exam",
        )


def validate_task_number(
    number_str: str, max_number: int
) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Validate task number selection.

    Args:
        number_str: Number string from user.
        max_number: Maximum valid task number.

    Returns:
        Tuple of (is_valid, task_number, error_message)
        - is_valid: True if number is valid
        - task_number: Integer task number if valid
        - error_message: Error message if invalid, None if valid
    """
    try:
        number = int(number_str.strip())
    except ValueError:
        return False, None, "❌ Please enter a valid number."

    if number < 1:
        return False, None, "❌ Task number must be at least 1."

    if number > max_number:
        return (
            False,
            None,
            f"❌ Task number must be between 1 and {max_number}.",
        )

    return True, number, None


def validate_confirmation(response: str) -> Tuple[bool, bool, Optional[str]]:
    """
    Validate yes/no confirmation response.

    Args:
        response: User's response string.

    Returns:
        Tuple of (is_valid, is_confirmed, error_message)
        - is_valid: True if response is valid
        - is_confirmed: True if user confirmed (YES), False if declined (NO)
        - error_message: Error message if invalid, None if valid
    """
    response = response.strip().upper()

    if response in ["YES", "Y", "CONFIRM", "OK", "SURE"]:
        return True, True, None
    elif response in ["NO", "N", "CANCEL", "NOPE"]:
        return True, False, None
    else:
        return (
            False,
            False,
            "❌ Please reply with YES to confirm or NO to cancel.",
        )


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.

    Args:
        text: Input text to sanitize.

    Returns:
        Sanitized text.
    """
    # Remove control characters
    text = "".join(char for char in text if char.isprintable() or char.isspace())

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
