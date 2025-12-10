"""
Unit tests for validator functions in StudyBuddy Telegram Bot.

Tests cover date validation, task title validation, and other input validators.
"""

from datetime import date, timedelta

import pytest

from utils.validators import (
    sanitize_input,
    validate_confirmation,
    validate_date,
    validate_task_number,
    validate_task_title,
    validate_task_type,
)


class TestValidateDate:
    """Test cases for date validation."""

    def test_valid_date_slash_format(self):
        """Test valid date with slash format (DD/MM/YYYY)."""
        is_valid, parsed_date, error = validate_date("25/12/2025")
        assert is_valid is True
        assert parsed_date == date(2025, 12, 25)
        assert error is None

    def test_valid_date_dot_format(self):
        """Test valid date with dot format (DD.MM.YYYY)."""
        is_valid, parsed_date, error = validate_date("15.03.2026")
        assert is_valid is True
        assert parsed_date == date(2026, 3, 15)
        assert error is None

    def test_valid_date_dash_format(self):
        """Test valid date with dash format (DD-MM-YYYY)."""
        is_valid, parsed_date, error = validate_date("01-01-2025")
        assert is_valid is True
        assert parsed_date == date(2025, 1, 1)
        assert error is None

    def test_invalid_date_format(self):
        """Test invalid date format."""
        is_valid, parsed_date, error = validate_date("2025/12/25")
        assert is_valid is False
        assert parsed_date is None
        assert "Invalid date format" in error

    def test_invalid_date_text(self):
        """Test non-date text input."""
        is_valid, parsed_date, error = validate_date("tomorrow")
        assert is_valid is False
        assert parsed_date is None
        assert error is not None

    def test_past_date(self):
        """Test date in the past."""
        yesterday = date.today() - timedelta(days=1)
        date_str = yesterday.strftime("%d/%m/%Y")
        is_valid, parsed_date, error = validate_date(date_str)
        assert is_valid is False
        assert parsed_date is None
        assert "must be in the future" in error

    def test_today_is_invalid(self):
        """Test that today's date is considered past."""
        today_str = date.today().strftime("%d/%m/%Y")
        is_valid, parsed_date, error = validate_date(today_str)
        assert is_valid is False
        assert "must be in the future" in error

    def test_far_future_date(self):
        """Test date too far in the future (>2 years)."""
        far_future = date.today() + timedelta(days=800)
        date_str = far_future.strftime("%d/%m/%Y")
        is_valid, parsed_date, error = validate_date(date_str)
        assert is_valid is False
        assert "too far in the future" in error

    def test_date_with_whitespace(self):
        """Test date with leading/trailing whitespace."""
        is_valid, parsed_date, error = validate_date("  25/12/2025  ")
        assert is_valid is True
        assert parsed_date == date(2025, 12, 25)

    def test_invalid_day(self):
        """Test invalid day (32)."""
        is_valid, parsed_date, error = validate_date("32/12/2025")
        assert is_valid is False
        assert error is not None

    def test_invalid_month(self):
        """Test invalid month (13)."""
        is_valid, parsed_date, error = validate_date("15/13/2025")
        assert is_valid is False
        assert error is not None


class TestValidateTaskTitle:
    """Test cases for task title validation."""

    def test_valid_title(self):
        """Test valid task title."""
        is_valid, sanitized, error = validate_task_title("Math Homework Chapter 5")
        assert is_valid is True
        assert sanitized == "Math Homework Chapter 5"
        assert error is None

    def test_empty_title(self):
        """Test empty title."""
        is_valid, sanitized, error = validate_task_title("")
        assert is_valid is False
        assert "cannot be empty" in error

    def test_whitespace_only_title(self):
        """Test title with only whitespace."""
        is_valid, sanitized, error = validate_task_title("   ")
        assert is_valid is False
        assert "cannot be empty" in error

    def test_title_too_long(self):
        """Test title exceeding maximum length."""
        long_title = "A" * 201
        is_valid, sanitized, error = validate_task_title(long_title, max_length=200)
        assert is_valid is False
        assert "too long" in error

    def test_title_too_short(self):
        """Test title below minimum length."""
        is_valid, sanitized, error = validate_task_title("AB")
        assert is_valid is False
        assert "too short" in error

    def test_title_with_multiple_spaces(self):
        """Test title with multiple consecutive spaces."""
        is_valid, sanitized, error = validate_task_title(
            "Math    Homework    Chapter 5"
        )
        assert is_valid is True
        assert sanitized == "Math Homework Chapter 5"
        assert error is None

    def test_title_with_leading_trailing_spaces(self):
        """Test title with leading and trailing spaces."""
        is_valid, sanitized, error = validate_task_title("  Math Homework  ")
        assert is_valid is True
        assert sanitized == "Math Homework"
        assert error is None

    def test_title_at_max_length(self):
        """Test title at exactly maximum length."""
        title = "A" * 200
        is_valid, sanitized, error = validate_task_title(title, max_length=200)
        assert is_valid is True
        assert len(sanitized) == 200
        assert error is None

    def test_title_with_special_characters(self):
        """Test title with special characters."""
        is_valid, sanitized, error = validate_task_title("Math #5 - Chapter 3.2")
        assert is_valid is True
        assert error is None


class TestValidateTaskType:
    """Test cases for task type validation."""

    def test_valid_assignment_number(self):
        """Test assignment selection with number 1."""
        is_valid, task_type, error = validate_task_type("1")
        assert is_valid is True
        assert task_type == "assignment"
        assert error is None

    def test_valid_exam_number(self):
        """Test exam selection with number 2."""
        is_valid, task_type, error = validate_task_type("2")
        assert is_valid is True
        assert task_type == "exam"
        assert error is None

    def test_valid_assignment_text(self):
        """Test assignment selection with text."""
        is_valid, task_type, error = validate_task_type("assignment")
        assert is_valid is True
        assert task_type == "assignment"

    def test_valid_exam_text(self):
        """Test exam selection with text."""
        is_valid, task_type, error = validate_task_type("exam")
        assert is_valid is True
        assert task_type == "exam"

    def test_valid_homework(self):
        """Test homework alias for assignment."""
        is_valid, task_type, error = validate_task_type("homework")
        assert is_valid is True
        assert task_type == "assignment"

    def test_valid_test(self):
        """Test test alias for exam."""
        is_valid, task_type, error = validate_task_type("test")
        assert is_valid is True
        assert task_type == "exam"

    def test_invalid_task_type(self):
        """Test invalid task type."""
        is_valid, task_type, error = validate_task_type("project")
        assert is_valid is False
        assert task_type is None
        assert "Invalid task type" in error

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        is_valid, task_type, error = validate_task_type("ASSIGNMENT")
        assert is_valid is True
        assert task_type == "assignment"

    def test_with_whitespace(self):
        """Test with leading/trailing whitespace."""
        is_valid, task_type, error = validate_task_type("  exam  ")
        assert is_valid is True
        assert task_type == "exam"


class TestValidateTaskNumber:
    """Test cases for task number validation."""

    def test_valid_number(self):
        """Test valid task number."""
        is_valid, number, error = validate_task_number("3", max_number=5)
        assert is_valid is True
        assert number == 3
        assert error is None

    def test_number_one(self):
        """Test minimum valid number (1)."""
        is_valid, number, error = validate_task_number("1", max_number=10)
        assert is_valid is True
        assert number == 1

    def test_max_number(self):
        """Test maximum valid number."""
        is_valid, number, error = validate_task_number("10", max_number=10)
        assert is_valid is True
        assert number == 10

    def test_number_too_large(self):
        """Test number exceeding maximum."""
        is_valid, number, error = validate_task_number("11", max_number=10)
        assert is_valid is False
        assert number is None
        assert "between 1 and 10" in error

    def test_zero(self):
        """Test zero (invalid)."""
        is_valid, number, error = validate_task_number("0", max_number=5)
        assert is_valid is False
        assert "must be at least 1" in error

    def test_negative_number(self):
        """Test negative number."""
        is_valid, number, error = validate_task_number("-1", max_number=5)
        assert is_valid is False
        assert "must be at least 1" in error

    def test_non_numeric(self):
        """Test non-numeric input."""
        is_valid, number, error = validate_task_number("abc", max_number=5)
        assert is_valid is False
        assert "valid number" in error

    def test_with_whitespace(self):
        """Test number with whitespace."""
        is_valid, number, error = validate_task_number("  3  ", max_number=5)
        assert is_valid is True
        assert number == 3


class TestValidateConfirmation:
    """Test cases for confirmation validation."""

    def test_yes(self):
        """Test YES confirmation."""
        is_valid, confirmed, error = validate_confirmation("YES")
        assert is_valid is True
        assert confirmed is True
        assert error is None

    def test_no(self):
        """Test NO confirmation."""
        is_valid, confirmed, error = validate_confirmation("NO")
        assert is_valid is True
        assert confirmed is False
        assert error is None

    def test_yes_lowercase(self):
        """Test yes in lowercase."""
        is_valid, confirmed, error = validate_confirmation("yes")
        assert is_valid is True
        assert confirmed is True

    def test_y_shorthand(self):
        """Test Y shorthand."""
        is_valid, confirmed, error = validate_confirmation("y")
        assert is_valid is True
        assert confirmed is True

    def test_n_shorthand(self):
        """Test N shorthand."""
        is_valid, confirmed, error = validate_confirmation("n")
        assert is_valid is True
        assert confirmed is False

    def test_confirm_alias(self):
        """Test CONFIRM alias."""
        is_valid, confirmed, error = validate_confirmation("confirm")
        assert is_valid is True
        assert confirmed is True

    def test_cancel_alias(self):
        """Test CANCEL alias."""
        is_valid, confirmed, error = validate_confirmation("cancel")
        assert is_valid is True
        assert confirmed is False

    def test_invalid_response(self):
        """Test invalid response."""
        is_valid, confirmed, error = validate_confirmation("maybe")
        assert is_valid is False
        assert "YES" in error and "NO" in error

    def test_with_whitespace(self):
        """Test with whitespace."""
        is_valid, confirmed, error = validate_confirmation("  YES  ")
        assert is_valid is True
        assert confirmed is True


class TestSanitizeInput:
    """Test cases for input sanitization."""

    def test_normal_text(self):
        """Test normal text remains unchanged."""
        result = sanitize_input("Hello World")
        assert result == "Hello World"

    def test_multiple_spaces(self):
        """Test multiple spaces are normalized."""
        result = sanitize_input("Hello    World")
        assert result == "Hello World"

    def test_leading_trailing_spaces(self):
        """Test leading and trailing spaces are removed."""
        result = sanitize_input("  Hello World  ")
        assert result == "Hello World"

    def test_newlines(self):
        """Test newlines are preserved as spaces."""
        result = sanitize_input("Hello\nWorld")
        assert "Hello" in result and "World" in result

    def test_tabs(self):
        """Test tabs are normalized."""
        result = sanitize_input("Hello\tWorld")
        assert result == "Hello World"

    def test_empty_string(self):
        """Test empty string."""
        result = sanitize_input("")
        assert result == ""

    def test_only_whitespace(self):
        """Test string with only whitespace."""
        result = sanitize_input("   \n\t  ")
        assert result == ""

    def test_special_characters(self):
        """Test special characters are preserved."""
        result = sanitize_input("Test @#$% 123")
        assert result == "Test @#$% 123"
