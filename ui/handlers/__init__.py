"""
UI Handlers Package

This package contains handler functions split by functionality:
- site.py: Site selection handlers
- submission.py: Task submission handlers
- task_management.py: Task management handlers (poll, delete, view)
- visibility.py: UI parameter visibility control
- ai_chat.py: AI chat and visual control handlers
"""

from ui.handlers.site import (
    update_model_dropdown,
    update_site_selection,
    save_token,
)

from ui.handlers.submission import (
    submit_task,
    confirm_send,
    cancel_send,
)

from ui.handlers.task_management import (
    manual_poll,
    get_task_detail,
    delete_selected_task,
)

from ui.handlers.visibility import (
    update_param_visibility,
)

from ui.handlers.ai_chat import (
    process_ai_chat_message,
    process_ai_chat_sync,
    clear_chat_history,
    get_example_prompts,
)

__all__ = [
    # Site handlers
    "update_model_dropdown",
    "update_site_selection",
    "save_token",
    # Submission handlers
    "submit_task",
    "confirm_send",
    "cancel_send",
    # Task management handlers
    "manual_poll",
    "get_task_detail",
    "delete_selected_task",
    # Visibility handlers
    "update_param_visibility",
    # AI Chat handlers
    "process_ai_chat_message",
    "process_ai_chat_sync",
    "clear_chat_history",
    "get_example_prompts",
]
