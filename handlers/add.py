"""
Add task command handler for StudyBuddy Telegram Bot.

This module handles the /add command with FSM (Finite State Machine)
for multi-step task creation flow.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models import Task, User
from keyboards.reply import get_main_menu_keyboard, get_task_type_keyboard
from states.task_states import AddTaskStates
from utils.formatters import format_task_confirmation
from utils.validators import validate_date, validate_task_title, validate_task_type

logger = logging.getLogger(__name__)

# Create router for add command
router = Router()


@router.message(F.text == "➕ Add Task")
@router.message(Command("add"))
async def cmd_add_start(message: Message, state: FSMContext):
    """
    Handle /add command - start task creation flow.

    Args:
        message: Incoming message object.
        state: FSM context for managing conversation state.
    """
    user_id = message.from_user.id

    # Update user's last_active timestamp
    await User.create_or_update(user_id=user_id)

    logger.info(f"User {user_id} started add task flow")

    # Clear any existing state
    await state.clear()

    # Ask for task type
    await message.answer(
        "Let's add a new task! 📝\n\nWhat type of task is this?",
        reply_markup=get_task_type_keyboard(),
    )

    # Set state to waiting for type
    await state.set_state(AddTaskStates.waiting_for_type)


@router.callback_query(
    AddTaskStates.waiting_for_type, F.data.in_(["type_assignment", "type_exam"])
)
async def process_task_type(callback: CallbackQuery, state: FSMContext):
    """
    Process task type selection from inline keyboard.

    Args:
        callback: Callback query from inline keyboard.
        state: FSM context.
    """
    # Extract task type from callback data
    task_type = "assignment" if callback.data == "type_assignment" else "exam"

    # Save task type to state
    await state.update_data(task_type=task_type)

    logger.info(f"User {callback.from_user.id} selected task type: {task_type}")

    # Answer callback to remove loading state
    await callback.answer()

    # Ask for task title
    task_type_display = "Assignment" if task_type == "assignment" else "Exam"
    await callback.message.answer(
        f"Great! Adding a new {task_type_display}. 📚\n\n"
        f"What's the name/title of this {task_type_display.lower()}?\n\n"
        f"<i>Example: Math Homework Chapter 5</i>",
        parse_mode="HTML",
    )

    # Delete the keyboard message
    await callback.message.delete()

    # Set state to waiting for title
    await state.set_state(AddTaskStates.waiting_for_title)


@router.message(AddTaskStates.waiting_for_type)
async def process_task_type_text(message: Message, state: FSMContext):
    """
    Handle text input for task type (fallback for users who type instead of clicking).

    Args:
        message: Incoming message object.
        state: FSM context.
    """
    user_input = message.text.strip()

    # Validate task type
    is_valid, task_type, error_message = validate_task_type(user_input)

    if not is_valid:
        await message.answer(
            error_message + "\n\nPlease use the buttons above or type 1 or 2.",
            reply_markup=get_task_type_keyboard(),
        )
        return

    # Save task type to state
    await state.update_data(task_type=task_type)

    logger.info(f"User {message.from_user.id} selected task type: {task_type}")

    # Ask for task title
    task_type_display = "Assignment" if task_type == "assignment" else "Exam"
    await message.answer(
        f"Great! Adding a new {task_type_display}. 📚\n\n"
        f"What's the name/title of this {task_type_display.lower()}?\n\n"
        f"<i>Example: Math Homework Chapter 5</i>",
        parse_mode="HTML",
    )

    # Set state to waiting for title
    await state.set_state(AddTaskStates.waiting_for_title)


@router.message(AddTaskStates.waiting_for_title)
async def process_task_title(message: Message, state: FSMContext):
    """
    Process task title input.

    Args:
        message: Incoming message object.
        state: FSM context.
    """
    user_input = message.text

    # Validate task title
    is_valid, sanitized_title, error_message = validate_task_title(user_input)

    if not is_valid:
        await message.answer(error_message + "\n\nPlease try again:")
        return

    # Save title to state
    await state.update_data(title=sanitized_title)

    logger.info(
        f"User {message.from_user.id} entered task title: {sanitized_title[:50]}"
    )

    # Ask for due date
    await message.answer(
        f"Perfect! ✅\n\n"
        f"When is this task due?\n\n"
        f"Please enter the date in <b>DD/MM/YYYY</b> format.\n\n"
        f"<i>Examples:\n"
        f"• 25/12/2025\n"
        f"• 15.03.2025\n"
        f"• 01/01/2026</i>",
        parse_mode="HTML",
    )

    # Set state to waiting for date
    await state.set_state(AddTaskStates.waiting_for_date)


@router.message(AddTaskStates.waiting_for_date)
async def process_due_date(message: Message, state: FSMContext):
    """
    Process due date input and create the task.

    Args:
        message: Incoming message object.
        state: FSM context.
    """
    user_input = message.text

    # Validate date
    is_valid, parsed_date, error_message = validate_date(user_input)

    if not is_valid:
        await message.answer(error_message + "\n\nPlease try again:")
        return

    # Get stored data from state
    data = await state.get_data()
    task_type = data.get("task_type")
    title = data.get("title")

    logger.info(
        f"User {message.from_user.id} entered due date: {parsed_date.isoformat()}"
    )

    # Create task in database
    try:
        task_id = await Task.create(
            user_id=message.from_user.id,
            task_type=task_type,
            title=title,
            due_date=parsed_date,
        )

        logger.info(f"Created task {task_id} for user {message.from_user.id}: {title}")

        # Send confirmation message
        confirmation_message = format_task_confirmation(task_type, title, parsed_date)
        await message.answer(
            confirmation_message, reply_markup=get_main_menu_keyboard()
        )

        # Clear state
        await state.clear()

        logger.info(f"User {message.from_user.id} completed add task flow")

    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        await message.answer(
            "❌ Oops! Something went wrong while saving your task.\n\n"
            "Please try again with /add"
        )
        await state.clear()


@router.message(Command("cancel"), StateFilter("*"))
async def cmd_cancel(message: Message, state: FSMContext):
    """
    Handle /cancel command to abort current operation.

    Args:
        message: Incoming message object.
        state: FSM context.
    """
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Nothing to cancel. You're not in the middle of any task.")
        return

    # Clear state
    await state.clear()

    logger.info(
        f"User {message.from_user.id} cancelled operation from state: {current_state}"
    )

    await message.answer(
        "❌ Operation cancelled.\n\n"
        "Use /add to create a new task or /help to see available commands."
    )
