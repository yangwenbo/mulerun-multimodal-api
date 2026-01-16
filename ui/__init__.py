"""
UI module for the multimodal API client
"""

from .helpers import (
    get_model_choices,
    get_model_choices_by_type,
    format_task_for_display,
    refresh_task_table,
    get_stats_text,
    build_params,
)

from .handlers import (
    update_model_dropdown,
    update_site_selection,
    save_token,
    submit_task,
    confirm_send,
    cancel_send,
    manual_poll,
    get_task_detail,
    delete_selected_task,
    update_param_visibility,
)

from .components import create_ui

__all__ = [
    # Helpers
    "get_model_choices",
    "get_model_choices_by_type",
    "format_task_for_display",
    "refresh_task_table",
    "get_stats_text",
    "build_params",
    # Handlers
    "update_model_dropdown",
    "update_site_selection",
    "save_token",
    "submit_task",
    "confirm_send",
    "cancel_send",
    "manual_poll",
    "get_task_detail",
    "delete_selected_task",
    "update_param_visibility",
    # Components
    "create_ui",
]
