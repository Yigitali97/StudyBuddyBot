"""
Finite State Machine (FSM) states for StudyBuddy bot.

This module defines conversation states for multi-step operations
like adding and deleting tasks.
"""

from aiogram.fsm.state import State, StatesGroup


class AddTaskStates(StatesGroup):
    """States for the add task conversation flow."""

    waiting_for_type = State()  # Waiting for task type selection
    waiting_for_title = State()  # Waiting for task title/name
    waiting_for_date = State()  # Waiting for due date


class DeleteTaskStates(StatesGroup):
    """States for the delete task conversation flow."""

    waiting_for_task_selection = State()  # Waiting for task number selection
    waiting_for_confirmation = State()  # Waiting for delete confirmation
