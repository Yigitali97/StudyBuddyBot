"""
Database models and CRUD operations for StudyBuddy.

This module provides data access layer for users and tasks.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from database.db import db

logger = logging.getLogger(__name__)


class User:
    """User model for database operations."""

    @staticmethod
    async def create_or_update(
        user_id: int, username: Optional[str] = None, first_name: Optional[str] = None
    ) -> None:
        """
        Create a new user or update existing user's last_active timestamp.

        Args:
            user_id: Telegram user ID.
            username: Telegram username.
            first_name: User's first name.
        """
        # Check if user exists
        existing_user = await db.fetch_one(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        )

        if existing_user:
            # Update last_active
            await db.execute(
                "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user_id,),
            )
            logger.info(f"Updated last_active for user {user_id}")
        else:
            # Create new user
            await db.execute(
                """
                INSERT INTO users (user_id, username, first_name, created_at, last_active)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """,
                (user_id, username, first_name),
            )
            logger.info(f"Created new user {user_id} ({first_name})")

    @staticmethod
    async def get(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.

        Args:
            user_id: Telegram user ID.

        Returns:
            User data as dictionary or None if not found.
        """
        row = await db.fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if row:
            return dict(row)
        return None

    @staticmethod
    async def get_all() -> List[Dict[str, Any]]:
        """
        Get all users.

        Returns:
            List of user dictionaries.
        """
        rows = await db.fetch_all("SELECT * FROM users")
        return [dict(row) for row in rows]


class Task:
    """Task model for database operations."""

    @staticmethod
    async def create(user_id: int, task_type: str, title: str, due_date: date) -> int:
        """
        Create a new task.

        Args:
            user_id: Telegram user ID.
            task_type: Type of task ('assignment' or 'exam').
            title: Task title/name.
            due_date: Task due date.

        Returns:
            ID of newly created task.
        """
        cursor = await db.execute(
            """
            INSERT INTO tasks (user_id, task_type, title, due_date, reminded, created_at)
            VALUES (?, ?, ?, ?, 0, CURRENT_TIMESTAMP)
            """,
            (user_id, task_type, title, due_date.isoformat()),
        )
        task_id = cursor.lastrowid
        logger.info(f"Created task {task_id} for user {user_id}: {title}")
        return task_id

    @staticmethod
    async def get_by_id(task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get task by ID.

        Args:
            task_id: Task ID.

        Returns:
            Task data as dictionary or None if not found.
        """
        row = await db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if row:
            return dict(row)
        return None

    @staticmethod
    async def get_user_tasks(
        user_id: int, include_past: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get all tasks for a user, sorted by due date.

        Args:
            user_id: Telegram user ID.
            include_past: Whether to include past tasks.

        Returns:
            List of task dictionaries sorted by due date (earliest first).
        """
        if include_past:
            query = """
                SELECT * FROM tasks
                WHERE user_id = ?
                ORDER BY due_date ASC
            """
        else:
            query = """
                SELECT * FROM tasks
                WHERE user_id = ? AND due_date >= DATE('now')
                ORDER BY due_date ASC
            """

        rows = await db.fetch_all(query, (user_id,))
        return [dict(row) for row in rows]

    @staticmethod
    async def delete(task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task ID to delete.

        Returns:
            True if task was deleted, False if not found.
        """
        # Check if task exists
        task = await Task.get_by_id(task_id)
        if not task:
            return False

        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        logger.info(f"Deleted task {task_id}")
        return True

    @staticmethod
    async def delete_user_task(user_id: int, task_id: int) -> bool:
        """
        Delete a task only if it belongs to the specified user.

        Args:
            user_id: Telegram user ID.
            task_id: Task ID to delete.

        Returns:
            True if task was deleted, False if not found or unauthorized.
        """
        # Verify task belongs to user
        task = await Task.get_by_id(task_id)
        if not task or task["user_id"] != user_id:
            return False

        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        logger.info(f"User {user_id} deleted task {task_id}")
        return True

    @staticmethod
    async def mark_as_reminded(task_id: int) -> None:
        """
        Mark a task as reminded to prevent duplicate reminders.

        Args:
            task_id: Task ID.
        """
        await db.execute("UPDATE tasks SET reminded = 1 WHERE id = ?", (task_id,))
        logger.info(f"Marked task {task_id} as reminded")

    @staticmethod
    async def get_tasks_needing_reminder() -> List[Dict[str, Any]]:
        """
        Get all tasks that need reminders (due in 24-25 hours and not yet reminded).

        Returns:
            List of task dictionaries that need reminders.
        """
        # Calculate time window: 24 to 25 hours from now
        now = datetime.now()
        reminder_start = (now + timedelta(hours=24)).date()
        reminder_end = (now + timedelta(hours=25)).date()

        query = """
            SELECT * FROM tasks
            WHERE reminded = 0
            AND due_date >= ?
            AND due_date < ?
            ORDER BY due_date ASC
        """

        rows = await db.fetch_all(
            query, (reminder_start.isoformat(), reminder_end.isoformat())
        )
        return [dict(row) for row in rows]

    @staticmethod
    async def update(
        task_id: int,
        task_type: Optional[str] = None,
        title: Optional[str] = None,
        due_date: Optional[date] = None,
    ) -> bool:
        """
        Update task fields.

        Args:
            task_id: Task ID to update.
            task_type: New task type (optional).
            title: New title (optional).
            due_date: New due date (optional).

        Returns:
            True if task was updated, False if not found.
        """
        # Check if task exists
        task = await Task.get_by_id(task_id)
        if not task:
            return False

        # Build update query dynamically based on provided fields
        updates = []
        params = []

        if task_type is not None:
            updates.append("task_type = ?")
            params.append(task_type)

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if due_date is not None:
            updates.append("due_date = ?")
            params.append(due_date.isoformat())
            # Reset reminded flag if date changes
            updates.append("reminded = 0")

        if not updates:
            return True  # Nothing to update

        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"

        await db.execute(query, tuple(params))
        logger.info(f"Updated task {task_id}")
        return True

    @staticmethod
    async def count_user_tasks(user_id: int) -> int:
        """
        Count total tasks for a user.

        Args:
            user_id: Telegram user ID.

        Returns:
            Number of tasks.
        """
        row = await db.fetch_one(
            "SELECT COUNT(*) as count FROM tasks WHERE user_id = ?", (user_id,)
        )
        return row["count"] if row else 0

    @staticmethod
    async def get_upcoming_tasks(user_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get tasks due within the next N days.

        Args:
            user_id: Telegram user ID.
            days: Number of days to look ahead.

        Returns:
            List of upcoming task dictionaries.
        """
        end_date = (datetime.now() + timedelta(days=days)).date()

        query = """
            SELECT * FROM tasks
            WHERE user_id = ?
            AND due_date >= DATE('now')
            AND due_date <= ?
            ORDER BY due_date ASC
        """

        rows = await db.fetch_all(query, (user_id, end_date.isoformat()))
        return [dict(row) for row in rows]
