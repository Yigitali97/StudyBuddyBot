"""
Database initialization and connection module for StudyBuddy.

This module handles database connection, schema creation, and database lifecycle management.
"""

import logging
import sqlite3
from typing import Optional

import aiosqlite

from config import Config

logger = logging.getLogger(__name__)


class Database:
    """Database manager for StudyBuddy bot."""

    def __init__(self, db_path: str = "studybuddy.db"):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path
        self._connection: Optional[aiosqlite.Connection] = None
        logger.info(f"Database manager initialized with path: {db_path}")

    async def connect(self) -> aiosqlite.Connection:
        """
        Establish database connection.

        Returns:
            aiosqlite.Connection: Active database connection.
        """
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
            logger.info("Database connection established")
        return self._connection

    async def disconnect(self):
        """Close database connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
            logger.info("Database connection closed")

    async def initialize(self):
        """
        Initialize database schema.

        Creates all necessary tables and indexes if they don't exist.
        """
        conn = await self.connect()

        # Create users table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create tasks table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_type TEXT NOT NULL,
                title TEXT NOT NULL,
                due_date DATE NOT NULL,
                reminded BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)

        # Create indexes for performance
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)
        """)

        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date)
        """)

        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_reminded ON tasks(reminded)
        """)

        await conn.commit()
        logger.info("Database schema initialized successfully")

    async def get_connection(self) -> aiosqlite.Connection:
        """
        Get active database connection.

        Returns:
            aiosqlite.Connection: Active database connection.
        """
        if self._connection is None:
            await self.connect()
        return self._connection

    async def execute(self, query: str, parameters: tuple = ()):
        """
        Execute a single SQL statement.

        Args:
            query: SQL query to execute.
            parameters: Query parameters.

        Returns:
            Cursor object.
        """
        conn = await self.get_connection()
        cursor = await conn.execute(query, parameters)
        await conn.commit()
        return cursor

    async def execute_many(self, query: str, parameters_list: list):
        """
        Execute a SQL statement multiple times.

        Args:
            query: SQL query to execute.
            parameters_list: List of parameter tuples.
        """
        conn = await self.get_connection()
        await conn.executemany(query, parameters_list)
        await conn.commit()

    async def fetch_one(self, query: str, parameters: tuple = ()):
        """
        Fetch a single row from the database.

        Args:
            query: SQL query to execute.
            parameters: Query parameters.

        Returns:
            Single row as aiosqlite.Row or None.
        """
        conn = await self.get_connection()
        cursor = await conn.execute(query, parameters)
        row = await cursor.fetchone()
        return row

    async def fetch_all(self, query: str, parameters: tuple = ()):
        """
        Fetch all rows from the database.

        Args:
            query: SQL query to execute.
            parameters: Query parameters.

        Returns:
            List of rows as aiosqlite.Row objects.
        """
        conn = await self.get_connection()
        cursor = await conn.execute(query, parameters)
        rows = await cursor.fetchall()
        return rows


# Global database instance
db = Database()
