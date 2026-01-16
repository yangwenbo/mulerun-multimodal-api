"""
UI Helper Functions
"""
import json
from config import MODELS, API_SITES, get_models_for_site
from core.database import get_all_tasks, get_task_stats


def get_model_choices():
    """Get model choices for dropdown"""
    return [(config["name"], key) for key, config in MODELS.items()]


def get_model_choices_by_type(task_type: str, site_key: str = "mulerun"):
    """Get model choices filtered by task type (video or image) and site"""
    # Get models available for the selected site
    site_models = get_models_for_site(site_key)

    if task_type == "video":
        # text2video and image2video
        return [(config["name"], key) for key, config in site_models.items()
                if config.get("type") in ("text2video", "image2video")]
    else:
        # text2image and image2image
        return [(config["name"], key) for key, config in site_models.items()
                if config.get("type") in ("text2image", "image2image")]


def format_task_for_display(task: dict) -> list:
    """Format a task record for table display"""
    status_emoji = {
        "pending": "🟡",
        "processing": "🔵",
        "completed": "🟢",
        "failed": "🔴"
    }

    created = task["created_at"][:19] if task["created_at"] else ""
    prompt = task["prompt"] or ""
    if len(prompt) > 50:
        prompt = prompt[:50] + "..."

    # Determine result type based on model
    model_config = MODELS.get(task["model_key"], {})
    is_image_task = model_config.get("type") in ("text2image", "image2image")
    result_type = "image(s)" if is_image_task else "video(s)"

    result_urls = task.get("result_urls", "")
    if result_urls:
        try:
            urls = json.loads(result_urls)
            result = f"{len(urls)} {result_type}"
        except Exception:
            result = ""
    else:
        result = ""

    return [
        task["id"],
        f"{status_emoji.get(task['status'], '⚪')} {task['status']}",
        task["model_name"],
        prompt,
        result,
        task.get("error_msg", "") or "",
        created
    ]


def refresh_task_table(site: str = "mulerun"):
    """Refresh the task table for a specific site"""
    tasks = get_all_tasks(limit=100, site=site)
    data = [format_task_for_display(t) for t in tasks]
    return data


def get_stats_text(site: str = "mulerun"):
    """Get statistics text for a specific site"""
    stats = get_task_stats(site=site)
    return f"Pending: {stats['pending']} | Processing: {stats['processing']} | Completed: {stats['completed']} | Failed: {stats['failed']}"


def build_params(
    model_key: str,
    prompt: str,
    negative_prompt: str,
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
    n_images: str
) -> dict:
    """Build params dict from UI inputs"""
    model_config = MODELS.get(model_key, {})
    params_def = model_config.get("params", {})

    params = {"prompt": prompt}

    # Add hidden params (like model name for wan2.5)
    for param_name, param_config in params_def.items():
        if param_config.get("type") == "hidden":
            params[param_name] = param_config.get("default")

    # 只添加模型定义中存在的参数
    if negative_prompt and "negative_prompt" in params_def:
        params["negative_prompt"] = negative_prompt
    if model_name and model_name != "default":
        if "model_name" in params_def:
            params["model_name"] = model_name
        elif "model" in params_def and params_def["model"].get("type") != "hidden":
            params["model"] = model_name
    if mode and "mode" in params_def:
        params["mode"] = mode
    if aspect_ratio and "aspect_ratio" in params_def:
        params["aspect_ratio"] = aspect_ratio
    if duration and "duration" in params_def:
        params["duration"] = duration
    if resolution and "resolution" in params_def:
        params["resolution"] = resolution
    if size and "size" in params_def:
        params["size"] = size
    if seconds and "seconds" in params_def:
        params["seconds"] = seconds
    if cfg_scale is not None and "cfg_scale" in params_def:
        params["cfg_scale"] = cfg_scale
    if video_type and "video_type" in params_def:
        params["video_type"] = video_type
    if audio and "audio" in params_def:
        params["audio"] = audio
    if audio_url and audio_url.strip() and "audio_url" in params_def:
        params["audio_url"] = audio_url.strip()
    if prompt_extend and "prompt_extend" in params_def:
        params["prompt_extend"] = prompt_extend
    if seed and seed.strip() and "seed" in params_def:
        params["seed"] = seed.strip()
    if n_images and "n" in params_def:
        params["n"] = n_images

    return params
