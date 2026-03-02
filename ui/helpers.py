"""
UI Helper Functions
"""
import re
import json
from config import MODELS, API_SITES, get_models_for_site
from core.database import get_all_tasks, get_task_stats


def convert_google_drive_url(url: str) -> str:
    """
    Convert Google Drive sharing link to direct access URL.

    Supports formats:
    - https://drive.google.com/file/d/FILE_ID/view?usp=sharing
    - https://drive.google.com/file/d/FILE_ID/view
    - https://drive.google.com/open?id=FILE_ID

    Returns direct link:
    - https://drive.google.com/uc?export=view&id=FILE_ID

    If not a Google Drive link, returns the original URL unchanged.
    """
    if not url:
        return url

    url = url.strip()

    # Pattern 1: /file/d/FILE_ID/view
    match = re.search(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"

    # Pattern 2: /open?id=FILE_ID
    match = re.search(r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"

    # Pattern 3: /uc?id=FILE_ID (already a direct link format, but ensure export=view)
    match = re.search(r'drive\.google\.com/uc\?.*id=([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"

    # Not a Google Drive link, return unchanged
    return url


def process_image_url(url: str) -> str:
    """
    Process image URL, converting Google Drive links to direct URLs.
    """
    return convert_google_drive_url(url)


def process_image_urls(urls: list) -> list:
    """
    Process a list of image URLs, converting any Google Drive links.
    """
    return [process_image_url(url) for url in urls]


def process_google_drive_url(url: str) -> str:
    """
    Process any URL, converting Google Drive links to direct URLs.
    Alias for convert_google_drive_url, can be used for audio/video URLs too.
    """
    return convert_google_drive_url(url)


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

    # Task UUID (API task ID)
    task_uuid = task.get("task_id", "") or ""

    return [
        task["id"],
        task_uuid,
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
    """Get statistics text for a specific site as HTML badges"""
    stats = get_task_stats(site=site)
    return f'''<div class="stats-container">
        <span class="stat-badge stat-pending">⏳ Pending: {stats['pending']}</span>
        <span class="stat-badge stat-processing">⚙️ Processing: {stats['processing']}</span>
        <span class="stat-badge stat-completed">✅ Completed: {stats['completed']}</span>
        <span class="stat-badge stat-failed">❌ Failed: {stats['failed']}</span>
    </div>'''


def build_params(
    model_key: str,
    prompt: str,
    negative_prompt: str,
    model_name: str,
    mode: str,
    aspect_ratio: str,
    duration: str,
    duration_int: int,
    resolution: str,
    size: str,
    seconds: str,
    cfg_scale: float,
    video_type: str,
    audio: str,
    audio_url: str,
    prompt_extend: str,
    web_search: str,
    seed: str,
    n_images: str,
    multi_shot: str = None,
    shot_type: str = None,
    multi_prompt: str = None
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
    if duration_int is not None and "duration_int" in params_def:
        params["duration"] = int(duration_int)
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
    # audio 组件同时用于 sound 参数（Kling v2.6/v3）
    if audio and "sound" in params_def:
        params["sound"] = audio
    if audio_url and audio_url.strip() and "audio_url" in params_def:
        # Process Google Drive links for audio URL
        params["audio_url"] = process_google_drive_url(audio_url.strip())
    if prompt_extend and "prompt_extend" in params_def:
        params["prompt_extend"] = prompt_extend
    if web_search and "web_search" in params_def:
        params["web_search"] = web_search
    if seed and seed.strip() and "seed" in params_def:
        params["seed"] = seed.strip()
    if n_images and "n" in params_def:
        params["n"] = n_images
    if multi_shot and "multi_shot" in params_def:
        # Convert string "true"/"false" to boolean
        params["multi_shot"] = multi_shot.lower() == "true"
    is_multi_shot = (multi_shot or "").lower() == "true"
    # shot_type 只在 multi_shot=true 时发送
    if is_multi_shot and shot_type and "shot_type" in params_def:
        params["shot_type"] = shot_type
    # intelligence: 用 prompt；customize: 用 multi_prompt
    is_intelligence = is_multi_shot and shot_type == "intelligence"
    is_customize = is_multi_shot and shot_type == "customize"
    if is_intelligence and prompt and "prompt" in params_def:
        params["prompt"] = prompt  # 已在开头设置，这里确保不被遗漏
    if is_customize and multi_prompt and multi_prompt.strip() and "multi_shot" in params_def:
        # multi_prompt is a JSON string: [{"index":0,"prompt":"...","duration":5},...]
        try:
            parsed = json.loads(multi_prompt.strip())
            if isinstance(parsed, list) and len(parsed) > 0:
                params["multi_prompt"] = parsed
        except (json.JSONDecodeError, ValueError):
            pass  # Invalid JSON — skip silently; server will validate
    # multi_shot=false 或 intelligence 模式下不发送 multi_prompt
    if not is_customize and "multi_prompt" in params:
        del params["multi_prompt"]
    # intelligence 模式下不发送 prompt 以外的冲突（prompt 已在 params["prompt"] 里）
    # customize 模式下不发送 prompt（服务端要求 multi_shot=true 时不能有 prompt）
    if is_customize and "prompt" in params:
        del params["prompt"]

    return params
