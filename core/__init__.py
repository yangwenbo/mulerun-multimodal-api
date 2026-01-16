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
]
