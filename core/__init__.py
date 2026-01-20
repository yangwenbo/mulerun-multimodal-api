"""
Core module for the multimodal API client
"""

from .api_client import APIClient, api_client
from .database import (
    init_db,
    get_connection,
    get_now_utc8,
    create_task,
    update_task_api_id,
    update_task_status,
    update_task_result,
    get_pending_tasks,
    get_all_tasks,
    get_task_by_id,
    get_task_by_uuid,
    delete_task,
    get_task_stats,
)
from .poller import TaskPoller, task_poller
from .ai_controller import (
    AICommandQueue,
    AIAction,
    ActionType,
    get_command_queue,
    create_action,
    parse_ai_response,
    queue_actions_from_response,
    create_status_action,
    create_highlight_action,
    create_click_action,
    create_select_action,
    create_type_action,
    create_clear_action,
    create_wait_action,
    ELEMENT_IDS,
    get_system_prompt_for_ui,
)

__all__ = [
    # API Client
    "APIClient",
    "api_client",
    # Database
    "init_db",
    "get_connection",
    "get_now_utc8",
    "create_task",
    "update_task_api_id",
    "update_task_status",
    "update_task_result",
    "get_pending_tasks",
    "get_all_tasks",
    "get_task_by_id",
    "get_task_by_uuid",
    "delete_task",
    "get_task_stats",
    # Poller
    "TaskPoller",
    "task_poller",
    # AI Controller
    "AICommandQueue",
    "AIAction",
    "ActionType",
    "get_command_queue",
    "create_action",
    "parse_ai_response",
    "queue_actions_from_response",
    "create_status_action",
    "create_highlight_action",
    "create_click_action",
    "create_select_action",
    "create_type_action",
    "create_clear_action",
    "create_wait_action",
    "ELEMENT_IDS",
    "get_system_prompt_for_ui",
]
