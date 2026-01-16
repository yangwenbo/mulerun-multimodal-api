"""
Site Selection Handlers
"""
import gradio as gr

from config import API_SITES
from ui.helpers import get_model_choices_by_type, refresh_task_table, get_stats_text


def update_model_dropdown(task_type: str, site_key: str = "mulerun"):
    """Update model dropdown based on task type and site selection"""
    choices = get_model_choices_by_type(task_type, site_key)
    return gr.update(choices=choices, value=None)


def update_site_selection(site_key: str, task_type: str):
    """Update API token, model dropdown, task table and stats when site changes"""
    site_config = API_SITES.get(site_key, API_SITES["mulerun"])
    token = site_config.get("token", "")
    site_name = site_config.get("name", site_key)

    # Get available models for this site and task type
    choices = get_model_choices_by_type(task_type, site_key)

    # Get task table data for this site
    task_data = refresh_task_table(site_key)
    stats = get_stats_text(site_key)

    # Update task history title
    title = f"### 📋 Task History ({site_name})"

    return (
        gr.update(value=token),  # Update API token
        gr.update(choices=choices, value=None),  # Update model dropdown
        task_data,  # Update task table
        stats,  # Update stats
        title  # Update title
    )


def save_token(token: str):
    """Save API token"""
    from core.api_client import APIClient
    global api_client
    api_client = APIClient(token)
    return "Token saved (for this session)"
