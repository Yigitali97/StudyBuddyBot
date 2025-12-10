"""
Delete task command handler for StudyBuddy Telegram Bot.

This module handles the /delete command with FSM (Finite State Machine)
for multi-step task deletion flow with confirmation.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models import Task, User
from keyboards.reply import get_confirmation_keyboard, get_main_menu_keyboard
from states.task_states import DeleteTaskStates
from utils.formatters import format_deletion_confirmation, format_task_selection_list
from utils.validators import validate_confirmation, validate_task_number

logger = logging.getLogger(__name__)

# Create router for delete command
router = Router()


@router.message(F.text == "🗑️ Delete Task")
@router.message(Command("delete"))
async def cmd_delete_start(message: Message, state: FSMContext):
    """
    Handle /delete command - start task deletion flow.

    Args:
        message: Incoming message object.
        state: FSM context for managing conversation state.
    """
    user_id = message.from_user.id

    # Update user's last_active timestamp
    await User.create_or_update(user_id=user_id)

    logger.info(f"User {user_id} started delete task flow")

    # Clear any existing state
    await state.clear()

    # Get all tasks for the user
    tasks = await Task.get_user_tasks(user_id=user_id, include_past=False)

    if not tasks:
        await message.answer(
            "You don't have any tasks to delete! 🎉\n\nUse /add to create a new task."
        )
        return

    # Format task selection list
    task_list = format_task_selection_list(tasks)

    # Store tasks in state for later reference
    await state.update_data(tasks=tasks)

    # Send task selection message
    await message.answer(
        f"🗑️ Delete a Task\n\n{task_list}\n\n"
        f"Please enter the number of the task you want to delete:"
    )

    # Set state to waiting for task selection
    await state.set_state(DeleteTaskStates.waiting_for_task_selection)


@router.message(DeleteTaskStates.waiting_for_task_selection)
async def process_task_selection(message: Message, state: FSMContext):
    """
    Process task number selection.

    Args:
        message: Incoming message object.
        state: FSM context.
    """
    user_input = message.text.strip()

    # Get tasks from state
    data = await state.get_data()
    tasks = data.get("tasks", [])

    if not tasks:
        await message.answer("❌ Error: No tasks found. Please start over with /delete")
        await state.clear()
        return

    # Validate task number
    is_valid, task_number, error_message = validate_task_number(user_input, len(tasks))

    if not is_valid:
        await message.answer(error_message + "\n\nPlease try again:")
        return

    # Get selected task (task_number is 1-based)
    selected_task = tasks[task_number - 1]

    # Save selected task to state
    await state.update_data(selected_task=selected_task)

    logger.info(
        f"User {message.from_user.id} selected task {selected_task['id']} for deletion"
    )

    # Format confirmation message
    confirmation_message = format_deletion_confirmation(selected_task)

    # Send confirmation request with inline keyboard
    await message.answer(confirmation_message, reply_markup=get_confirmation_keyboard())

    # Set state to waiting for confirmation
    await state.set_state(DeleteTaskStates.waiting_for_confirmation)


@router.callback_query(
    DeleteTaskStates.waiting_for_confirmation,
    F.data.in_(["confirm_yes", "confirm_no"]),
)
async def process_confirmation_callback(callback: CallbackQuery, state: FSMContext):
    """
    Process confirmation from inline keyboard buttons.

    Args:
        callback: Callback query from inline keyboard.
        state: FSM context.
    """
    user_id = callback.from_user.id

    # Answer callback to remove loading state
    await callback.answer()

    if callback.data == "confirm_yes":
        # User confirmed deletion
        data = await state.get_data()
        selected_task = data.get("selected_task")

        if not selected_task:
            await callback.message.answer(
                "❌ Error: Task not found. Please start over with /delete"
            )
            await state.clear()
            return

        # Delete the task
        success = await Task.delete_user_task(user_id, selected_task["id"])

        if success:
            logger.info(f"User {user_id} deleted task {selected_task['id']}")

            await callback.message.answer(
                f"✅ Task Deleted Successfully!\n\n"
                f"🗑️ {selected_task['title']}\n\n"
                f"Use /list to view your remaining tasks.",
                reply_markup=get_main_menu_keyboard(),
            )
        else:
            logger.warning(
                f"User {user_id} failed to delete task {selected_task['id']}"
            )
            await callback.message.answer(
                "❌ Failed to delete task. It may have already been removed.\n\n"
                "Use /list to check your current tasks.",
                reply_markup=get_main_menu_keyboard(),
            )

        # Delete the confirmation message
        await callback.message.delete()

        # Clear state
        await state.clear()

    else:
        # User cancelled deletion
        logger.info(f"User {user_id} cancelled task deletion")

        await callback.message.answer(
            "❌ Deletion cancelled. Your task is safe! 😊\n\n"
            "Use /delete to try again or /list to view your tasks.",
            reply_markup=get_main_menu_keyboard(),
        )

        # Delete the confirmation message
        await callback.message.delete()

        # Clear state
        await state.clear()


@router.message(DeleteTaskStates.waiting_for_confirmation)
async def process_confirmation_text(message: Message, state: FSMContext):
    """
    Process text confirmation (fallback for users who type instead of clicking).

    Args:
        message: Incoming message object.
        state: FSM context.
    """
    user_input = message.text.strip()
    user_id = message.from_user.id

    # Validate confirmation
    is_valid, is_confirmed, error_message = validate_confirmation(user_input)

    if not is_valid:
        await message.answer(
            error_message + "\n\nOr use the buttons above.",
            reply_markup=get_confirmation_keyboard(),
        )
        return

    if is_confirmed:
        # User confirmed deletion
        data = await state.get_data()
        selected_task = data.get("selected_task")

        if not selected_task:
            await message.answer(
                "❌ Error: Task not found. Please start over with /delete"
            )
            await state.clear()
            return

        # Delete the task
        success = await Task.delete_user_task(user_id, selected_task["id"])

        if success:
            logger.info(f"User {user_id} deleted task {selected_task['id']}")

            await message.answer(
                f"✅ Task Deleted Successfully!\n\n"
                f"🗑️ {selected_task['title']}\n\n"
                f"Use /list to view your remaining tasks.",
                reply_markup=get_main_menu_keyboard(),
            )
        else:
            logger.warning(
                f"User {user_id} failed to delete task {selected_task['id']}"
            )
            await message.answer(
                "❌ Failed to delete task. It may have already been removed.\n\n"
                "Use /list to check your current tasks.",
                reply_markup=get_main_menu_keyboard(),
            )

        # Clear state
        await state.clear()

    else:
        # User cancelled deletion
        logger.info(f"User {user_id} cancelled task deletion")

        await message.answer(
            "❌ Deletion cancelled. Your task is safe! 😊\n\n"
            "Use /delete to try again or /list to view your tasks.",
            reply_markup=get_main_menu_keyboard(),
        )

        # Clear state
        await state.clear()
