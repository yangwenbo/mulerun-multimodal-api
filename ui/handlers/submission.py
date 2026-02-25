"""
Task Submission Handlers
"""
import json
import gradio as gr

from config import API_SITES, get_models_for_site
from core.api_client import APIClient
from core.database import (
    create_task,
    update_task_api_id,
    update_task_status,
)
from ui.helpers import refresh_task_table, get_stats_text, build_params, process_image_url, process_image_urls


def submit_task(
    model_key: str,
    prompt: str,
    negative_prompt: str,
    image,
    image_url: str,
    multi_images,
    multi_images_url: str,
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
    seed: str,
    n_images: str,
    multi_shot: str,
    shot_type: str,
    multi_prompt: str,
    last_frame,
    last_frame_url: str,
    reference_images,
    reference_images_url: str,
    api_token: str,
    debug_mode: bool,
    site_key: str,
    proxy: str = ""
):
    """Submit a video generation task (or preview in debug mode)"""
    print(f"[DEBUG] submit_task called with model_key: {model_key}, site: {site_key}, proxy: {proxy}")

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
    # URL input takes priority over file upload
    # Google Drive URLs are automatically converted to direct links
    is_multi_image = model_config.get("multi_image", False)
    if is_multi_image:
        # Multi-image model: URL takes priority, then Gallery upload
        if multi_images_url and multi_images_url.strip():
            # Parse URLs from text (one per line) and process Google Drive links
            image_paths = process_image_urls([url.strip() for url in multi_images_url.strip().split('\n') if url.strip()])
        elif multi_images:
            # Extract file paths from multi_images Gallery
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

        # Check required
        if "image" in params_def and params_def["image"].get("required") and not image_paths:
            return ("At least one image is required for this model", refresh_task_table(site_key), get_stats_text(site_key),
                    gr.update(visible=False, value=""), None,
                    gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))
    else:
        # Single image model: URL takes priority
        if image_url and image_url.strip():
            # Process Google Drive link
            image_paths = [process_image_url(image_url.strip())]
        elif image:
            image_paths = [image]
        else:
            image_paths = []

        # Check required
        if "image" in params_def and params_def["image"].get("required") and not image_paths:
            return ("Image is required for this model", refresh_task_table(site_key), get_stats_text(site_key),
                    gr.update(visible=False, value=""), None,
                    gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    # Handle last_frame (veo3 interpolation) - URL takes priority
    if last_frame_url and last_frame_url.strip():
        # Process Google Drive link
        last_frame_path = process_image_url(last_frame_url.strip())
    else:
        last_frame_path = last_frame if last_frame else None

    # Handle reference_images (veo3) - URL takes priority
    if reference_images_url and reference_images_url.strip():
        # Process Google Drive links
        reference_image_paths = process_image_urls([url.strip() for url in reference_images_url.strip().split('\n') if url.strip()])
    elif reference_images:
        reference_image_paths = []
        for item in reference_images:
            if isinstance(item, tuple):
                reference_image_paths.append(item[0])
            elif isinstance(item, dict) and 'name' in item:
                reference_image_paths.append(item['name'])
            elif hasattr(item, 'name'):
                reference_image_paths.append(item.name)
            else:
                reference_image_paths.append(str(item))
    else:
        reference_image_paths = []

    # Build params
    params = build_params(
        model_key, prompt, negative_prompt, model_name, mode, aspect_ratio,
        duration, duration_int, resolution, size, seconds, cfg_scale, video_type,
        audio, audio_url, prompt_extend, seed, n_images, multi_shot, shot_type, multi_prompt
    )

    # Create extra_images dict for special image parameters
    extra_images = {}
    if last_frame_path:
        extra_images["last_frame"] = last_frame_path
    if reference_image_paths:
        extra_images["reference_images"] = reference_image_paths

    client = APIClient(api_token, base_url, proxy)

    # Debug mode: show preview and wait for confirmation
    if debug_mode:
        success, error, request_info = client.get_request_preview(
            model_key=model_key,
            params=params,
            image_paths=image_paths,
            model_config=model_config,
            extra_images=extra_images
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
            "extra_images": extra_images,
            "api_token": api_token,
            "base_url": base_url,
            "model_config": model_config,
            "site": site_key,
            "proxy": proxy
        }

        return ("Review the request below and click 'Confirm Send' to proceed",
                refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=True, value=preview_text), pending_data,
                gr.update(visible=False), gr.update(visible=True), gr.update(visible=True))

    # Normal mode: submit directly
    return _do_submit(model_key, model_config["name"], prompt, params, image_paths, extra_images, api_token, base_url, model_config, site_key, proxy)


def _do_submit(model_key, model_name, prompt, params, image_paths, extra_images, api_token, base_url, model_config, site, proxy=""):
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
    client = APIClient(api_token, base_url, proxy)
    success, message, api_task_id = client.submit_task(
        model_key=model_key,
        params=params,
        image_paths=image_paths,
        model_config=model_config,
        extra_images=extra_images
    )

    if success and api_task_id:
        update_task_api_id(local_id, api_task_id)
        result_msg = f"Task submitted successfully! ID: {local_id}, API Task: {api_task_id}"
        return (result_msg, refresh_task_table(site), get_stats_text(site),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))
    else:
        update_task_status(local_id, "failed", message)
        result_msg = f"Failed to submit (ID: {local_id})"
        return (result_msg, refresh_task_table(site), get_stats_text(site),
                gr.update(visible=True, value=message), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))


def confirm_send(pending_request):
    """Confirm and send the pending request"""
    if not pending_request:
        return ("No pending request", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    site = pending_request.get("site", "mulerun")
    extra_images = pending_request.get("extra_images", {})
    proxy = pending_request.get("proxy", "")
    return _do_submit(
        pending_request["model_key"],
        pending_request["model_name"],
        pending_request["prompt"],
        pending_request["params"],
        pending_request["image_paths"],
        extra_images,
        pending_request["api_token"],
        pending_request["base_url"],
        pending_request["model_config"],
        site,
        proxy
    )


def cancel_send(site_key: str = "mulerun"):
    """Cancel the pending request"""
    return ("Request cancelled", refresh_task_table(site_key), get_stats_text(site_key),
            gr.update(visible=False, value=""), None,
            gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))
