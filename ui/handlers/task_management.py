"""
Task Management Handlers
"""
import json

from config import MODELS, API_SITES, get_models_for_site
from core.api_client import APIClient
from core.database import (
    update_task_status,
    update_task_result,
    update_task_local_paths,
    get_task_by_id,
    get_task_by_uuid,
    delete_task,
)
from core.media_manager import media_manager
from ui.helpers import refresh_task_table, get_stats_text


def _resolve_task(task_id: int, task_uuid: str):
    """Resolve task from either ID or UUID"""
    task = None
    if task_id and task_id > 0:
        task = get_task_by_id(int(task_id))
    if not task and task_uuid and task_uuid.strip():
        task = get_task_by_uuid(task_uuid.strip())
    return task


def manual_poll(task_id: int, task_uuid: str, api_token: str, site_key: str, proxy: str = ""):
    """Manually poll a task"""
    if not api_token:
        return "Please enter API Token", refresh_task_table(site_key), get_stats_text(site_key)

    task = _resolve_task(task_id, task_uuid)
    if not task:
        return "Task not found (check Task ID or Task UUID)", refresh_task_table(site_key), get_stats_text(site_key)

    if not task["task_id"]:
        return "Task has no API task ID", refresh_task_table(site_key), get_stats_text(site_key)

    # Get site configuration
    site_config = API_SITES.get(site_key, API_SITES["mulerun"])
    base_url = site_config.get("base_url")

    # Get site-specific model config
    site_models = get_models_for_site(site_key)
    model_config = site_models.get(task["model_key"])

    client = APIClient(api_token, base_url, proxy)
    status, videos, error = client.get_task_status(task["model_key"], task["task_id"], model_config)

    if status == "completed":
        # Determine media type based on model config
        model_base_config = MODELS.get(task["model_key"], {})
        is_image_task = model_base_config.get("type") in ("text2image", "image2image")
        media_type = "image" if is_image_task else "video"

        # Download media to local storage
        local_paths = media_manager.download_media(task["id"], videos or [], media_type)

        # Update database with both remote URLs and local paths
        update_task_result(task["id"], videos or [], local_paths if local_paths else None)

        downloaded_count = len([p for p in local_paths if p]) if local_paths else 0
        return f"Task completed! {len(videos or [])} {media_type}(s), downloaded {downloaded_count} files", refresh_task_table(site_key), get_stats_text(site_key)
    elif status == "failed":
        update_task_status(task["id"], "failed", error)
        return f"Task failed: {error}", refresh_task_table(site_key), get_stats_text(site_key)
    else:
        return f"Task status: {status}", refresh_task_table(site_key), get_stats_text(site_key)


def get_task_detail(task_id: int, task_uuid: str):
    """Get task details for preview"""
    task = _resolve_task(task_id, task_uuid)
    if not task:
        return "Task not found (enter Task ID or Task UUID)", None, [], "", ""

    # Build info text
    info = f"""
**Task ID:** {task['id']}
**Model:** {task['model_name']}
**Status:** {task['status']}
**API Task ID:** {task.get('task_id', 'N/A')}
**Created:** {task['created_at']}
**Updated:** {task['updated_at']}

**Prompt:**
{task['prompt'] or 'N/A'}

**Parameters:**
```json
{task['params']}
```
"""

    if task.get("error_msg"):
        info += f"\n**Error:** {task['error_msg']}"

    # Determine if this is an image or video task based on model type
    model_config = MODELS.get(task['model_key'], {})
    is_image_task = model_config.get("type") in ("text2image", "image2image")
    media_type = "image" if is_image_task else "video"

    # Get result URLs and local paths
    video_urls = []
    image_urls = []
    result_links = ""
    first_video_url = None
    video_urls_text = ""

    if task.get("result_urls"):
        try:
            urls = json.loads(task["result_urls"])
            local_paths = json.loads(task.get("local_paths") or "[]") if task.get("local_paths") else []

            # Get media paths (prefer local, fallback to remote)
            media_paths, needs_update = media_manager.get_media_paths(
                task["id"], urls, local_paths, media_type
            )

            # Update local_paths in database if new downloads occurred
            if needs_update:
                update_task_local_paths(task["id"], media_paths)

            # Use media_paths for display (local paths or remote URLs)
            result_links = "\n".join(urls)  # Always show original URLs in result_links
            if media_paths:
                if is_image_task:
                    image_urls = [(path, f"Image {i+1}") for i, path in enumerate(media_paths)]
                else:
                    video_urls = media_paths
                    first_video_url = media_paths[0] if media_paths else None
                    video_urls_text = "\n".join([f"Video {i+1}: {path}" for i, path in enumerate(media_paths)])
        except Exception:
            pass

    return info, first_video_url, image_urls, video_urls_text, result_links


def delete_selected_task(task_id: int, task_uuid: str, site_key: str):
    """Delete a task and its local media files"""
    task = _resolve_task(task_id, task_uuid)
    if task:
        # Clean up local media files
        media_manager.cleanup_task_media(task["id"])
        # Delete task from database
        delete_task(task["id"])
        return f"Task {task['id']} deleted (including local media)", refresh_task_table(site_key), get_stats_text(site_key)
    return "No task selected (enter Task ID or Task UUID)", refresh_task_table(site_key), get_stats_text(site_key)
