"""
UI Event Handlers
"""
import json
import gradio as gr

from config import MODELS, API_SITES, get_models_for_site
from core.api_client import APIClient
from core.database import (
    create_task,
    update_task_api_id,
    update_task_status,
    update_task_result,
    update_task_local_paths,
    get_task_by_id,
    get_task_by_uuid,
    delete_task,
)
from core.media_manager import media_manager
from ui.helpers import (
    get_model_choices_by_type,
    refresh_task_table,
    get_stats_text,
    build_params,
)


# ============== Site Selection ==============

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
    title = f"### Task History ({site_name})"

    return (
        gr.update(value=token),  # Update API token
        gr.update(choices=choices, value=None),  # Update model dropdown
        task_data,  # Update task table
        stats,  # Update stats
        title  # Update title
    )


# ============== API Token ==============

def save_token(token: str):
    """Save API token"""
    from core.api_client import APIClient
    global api_client
    api_client = APIClient(token)
    return "Token saved (for this session)"


# ============== Task Submission ==============

def submit_task(
    model_key: str,
    prompt: str,
    negative_prompt: str,
    image,
    multi_images,
    model_name: str,
    mode: str,
    aspect_ratio: str,
    duration: str,
    resolution: str,
    size: str,
    seconds: str,
    cfg_scale: float,
    video_type: str,
    audio: str,
    audio_url: str,
    prompt_extend: str,
    seed: str,
    n_images: str,
    api_token: str,
    debug_mode: bool,
    site_key: str
):
    """Submit a video generation task (or preview in debug mode)"""
    print(f"[DEBUG] submit_task called with model_key: {model_key}, site: {site_key}")

    # Get site configuration
    site_config = API_SITES.get(site_key, API_SITES["mulerun"])
    base_url = site_config.get("base_url")

    # Get site-specific model config (with potential endpoint overrides)
    site_models = get_models_for_site(site_key)

    if not api_token:
        return ("Please enter API Token first", refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    if not model_key:
        return ("Please select a model", refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    # Use site-specific model config
    model_config = site_models.get(model_key)
    if not model_config:
        return (f"Model {model_key} not available for site {site_key}", refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    # Check required fields
    params_def = model_config["params"]
    if "prompt" in params_def and params_def["prompt"].get("required") and not prompt:
        return ("Prompt is required", refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    # Determine image paths based on model type (single vs multi-image)
    is_multi_image = model_config.get("multi_image", False)
    if is_multi_image:
        # Multi-image model: use multi_images (from Gallery component)
        if "image" in params_def and params_def["image"].get("required") and not multi_images:
            return ("At least one image is required for this model", refresh_task_table(site_key), get_stats_text(site_key),
                    gr.update(visible=False, value=""), None,
                    gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))
        # Extract file paths from multi_images
        if multi_images:
            image_paths = []
            for item in multi_images:
                if isinstance(item, tuple):
                    image_paths.append(item[0])
                elif isinstance(item, dict) and 'name' in item:
                    image_paths.append(item['name'])
                elif hasattr(item, 'name'):
                    image_paths.append(item.name)
                else:
                    image_paths.append(str(item))
        else:
            image_paths = []
    else:
        # Single image model
        if "image" in params_def and params_def["image"].get("required") and not image:
            return ("Image is required for this model", refresh_task_table(site_key), get_stats_text(site_key),
                    gr.update(visible=False, value=""), None,
                    gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))
        image_paths = [image] if image else []

    # Build params
    params = build_params(
        model_key, prompt, negative_prompt, model_name, mode, aspect_ratio,
        duration, resolution, size, seconds, cfg_scale, video_type,
        audio, audio_url, prompt_extend, seed, n_images
    )

    client = APIClient(api_token, base_url)

    # Debug mode: show preview and wait for confirmation
    if debug_mode:
        success, error, request_info = client.get_request_preview(
            model_key=model_key,
            params=params,
            image_paths=image_paths,
            model_config=model_config
        )

        if not success:
            return (f"Error: {error}", refresh_task_table(site_key), get_stats_text(site_key),
                    gr.update(visible=False, value=""), None,
                    gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

        # Format preview with model info for debugging
        preview_data = {
            "selected_model": model_key,
            "request": request_info
        }
        preview_text = json.dumps(preview_data, indent=2, ensure_ascii=False)

        # Store pending request data
        pending_data = {
            "model_key": model_key,
            "model_name": model_config["name"],
            "prompt": prompt,
            "params": params,
            "image_paths": image_paths,
            "api_token": api_token,
            "base_url": base_url,
            "model_config": model_config,
            "site": site_key
        }

        return ("Review the request below and click 'Confirm Send' to proceed",
                refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=True, value=preview_text), pending_data,
                gr.update(visible=False), gr.update(visible=True), gr.update(visible=True))

    # Normal mode: submit directly
    return _do_submit(model_key, model_config["name"], prompt, params, image_paths, api_token, base_url, model_config, site_key)


def _do_submit(model_key, model_name, prompt, params, image_paths, api_token, base_url, model_config, site):
    """Actually submit the task to API"""
    # Create local task record first
    image_path_for_db = ",".join(image_paths) if image_paths else None
    local_id = create_task(
        model_key=model_key,
        model_name=model_name,
        prompt=prompt,
        params=params,
        image_path=image_path_for_db,
        api_token=api_token,
        site=site
    )

    # Submit to API
    client = APIClient(api_token, base_url)
    success, message, api_task_id = client.submit_task(
        model_key=model_key,
        params=params,
        image_paths=image_paths,
        model_config=model_config
    )

    if success and api_task_id:
        update_task_api_id(local_id, api_task_id)
        result_msg = f"Task submitted successfully! ID: {local_id}, API Task: {api_task_id}"
    else:
        update_task_status(local_id, "failed", message)
        result_msg = f"Failed to submit: {message}"

    return (result_msg, refresh_task_table(site), get_stats_text(site),
            gr.update(visible=False, value=""), None,
            gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))


def confirm_send(pending_request):
    """Confirm and send the pending request"""
    if not pending_request:
        return ("No pending request", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    site = pending_request.get("site", "mulerun")
    return _do_submit(
        pending_request["model_key"],
        pending_request["model_name"],
        pending_request["prompt"],
        pending_request["params"],
        pending_request["image_paths"],
        pending_request["api_token"],
        pending_request["base_url"],
        pending_request["model_config"],
        site
    )


def cancel_send(site_key: str = "mulerun"):
    """Cancel the pending request"""
    return ("Request cancelled", refresh_task_table(site_key), get_stats_text(site_key),
            gr.update(visible=False, value=""), None,
            gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))


# ============== Task Management ==============

def _resolve_task(task_id: int, task_uuid: str):
    """Resolve task from either ID or UUID"""
    task = None
    if task_id and task_id > 0:
        task = get_task_by_id(int(task_id))
    if not task and task_uuid and task_uuid.strip():
        task = get_task_by_uuid(task_uuid.strip())
    return task


def manual_poll(task_id: int, task_uuid: str, api_token: str, site_key: str):
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

    client = APIClient(api_token, base_url)
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


# ============== UI Visibility Control ==============

def update_param_visibility(model_key: str):
    """Update parameter visibility based on selected model"""
    if not model_key or model_key not in MODELS:
        return [gr.update(visible=False)] * 18

    model_config = MODELS[model_key]
    params = model_config["params"]

    updates = []

    # prompt
    if "prompt" in params:
        prompt_label = params["prompt"].get("label", "Prompt")
        updates.append(gr.update(visible=True, label=prompt_label))
    else:
        updates.append(gr.update(visible=False))

    # negative_prompt
    if "negative_prompt" in params:
        neg_prompt_label = params["negative_prompt"].get("label", "Negative Prompt")
        updates.append(gr.update(visible=True, label=neg_prompt_label))
    else:
        updates.append(gr.update(visible=False))

    # image (single image) - hide if model supports multi_image
    if "image" in params and not model_config.get("multi_image"):
        image_label = params["image"].get("label", "Input Image")
        updates.append(gr.update(visible=True, label=image_label))
    else:
        updates.append(gr.update(visible=False))

    # multi_images (multiple images) - show if model supports multi_image
    if "image" in params and model_config.get("multi_image"):
        image_label = params["image"].get("label", "Input Images")
        max_images = model_config.get("max_images", 10)
        updates.append(gr.update(visible=True, label=f"{image_label} (最多{max_images}张)"))
    else:
        updates.append(gr.update(visible=False))

    # model_name / model (skip hidden type)
    has_model = ("model_name" in params or "model" in params)
    model_param = params.get("model_name") or params.get("model") or {}
    if has_model and model_param.get("type") != "hidden":
        choices = model_param.get("options", [])
        default = model_param.get("default", "")
        updates.append(gr.update(visible=True, choices=choices, value=default))
    else:
        updates.append(gr.update(visible=False))

    # mode
    if "mode" in params:
        updates.append(gr.update(visible=True, choices=params["mode"]["options"], value=params["mode"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # aspect_ratio
    if "aspect_ratio" in params:
        updates.append(gr.update(visible=True, choices=params["aspect_ratio"]["options"], value=params["aspect_ratio"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # duration
    if "duration" in params:
        updates.append(gr.update(visible=True, choices=params["duration"]["options"], value=params["duration"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # resolution (veo3, wan2.5-i2v)
    if "resolution" in params:
        updates.append(gr.update(visible=True, choices=params["resolution"]["options"], value=params["resolution"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # size (sora, wan2.5-t2v, wan2.5-t2i)
    if "size" in params:
        updates.append(gr.update(visible=True, choices=params["size"]["options"], value=params["size"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # seconds (sora)
    if "seconds" in params:
        updates.append(gr.update(visible=True, choices=params["seconds"]["options"], value=params["seconds"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # cfg_scale
    if "cfg_scale" in params:
        updates.append(gr.update(visible=True, value=params["cfg_scale"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # video_type (midjourney)
    if "video_type" in params:
        updates.append(gr.update(visible=True, choices=params["video_type"]["options"], value=params["video_type"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # audio (wan2.5)
    if "audio" in params:
        updates.append(gr.update(visible=True, choices=params["audio"]["options"], value=params["audio"]["default"], label=params["audio"].get("label", "Audio")))
    else:
        updates.append(gr.update(visible=False))

    # audio_url (wan2.5)
    if "audio_url" in params:
        updates.append(gr.update(visible=True, label=params["audio_url"].get("label", "Audio URL")))
    else:
        updates.append(gr.update(visible=False))

    # prompt_extend (wan2.5)
    if "prompt_extend" in params:
        updates.append(gr.update(visible=True, choices=params["prompt_extend"]["options"], value=params["prompt_extend"]["default"], label=params["prompt_extend"].get("label", "Prompt Extend")))
    else:
        updates.append(gr.update(visible=False))

    # seed (wan2.5)
    if "seed" in params:
        updates.append(gr.update(visible=True, label=params["seed"].get("label", "Seed")))
    else:
        updates.append(gr.update(visible=False))

    # n (wan2.5 t2i - number of images)
    if "n" in params:
        updates.append(gr.update(visible=True, choices=params["n"]["options"], value=params["n"]["default"], label=params["n"].get("label", "Number of Images")))
    else:
        updates.append(gr.update(visible=False))

    return updates
