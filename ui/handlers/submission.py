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
from ui.helpers import refresh_task_table, get_stats_text, build_params


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
    shot_type: str,
    last_frame,
    reference_images,
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

    # Handle last_frame (veo3 interpolation)
    last_frame_path = last_frame if last_frame else None

    # Handle reference_images (veo3)
    reference_image_paths = []
    if reference_images:
        for item in reference_images:
            if isinstance(item, tuple):
                reference_image_paths.append(item[0])
            elif isinstance(item, dict) and 'name' in item:
                reference_image_paths.append(item['name'])
            elif hasattr(item, 'name'):
                reference_image_paths.append(item.name)
            else:
                reference_image_paths.append(str(item))

    # Build params
    params = build_params(
        model_key, prompt, negative_prompt, model_name, mode, aspect_ratio,
        duration, resolution, size, seconds, cfg_scale, video_type,
        audio, audio_url, prompt_extend, seed, n_images, shot_type
    )

    # Create extra_images dict for special image parameters
    extra_images = {}
    if last_frame_path:
        extra_images["last_frame"] = last_frame_path
    if reference_image_paths:
        extra_images["reference_images"] = reference_image_paths

    client = APIClient(api_token, base_url)

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
            "site": site_key
        }

        return ("Review the request below and click 'Confirm Send' to proceed",
                refresh_task_table(site_key), get_stats_text(site_key),
                gr.update(visible=True, value=preview_text), pending_data,
                gr.update(visible=False), gr.update(visible=True), gr.update(visible=True))

    # Normal mode: submit directly
    return _do_submit(model_key, model_config["name"], prompt, params, image_paths, extra_images, api_token, base_url, model_config, site_key)


def _do_submit(model_key, model_name, prompt, params, image_paths, extra_images, api_token, base_url, model_config, site):
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
        model_config=model_config,
        extra_images=extra_images
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
    extra_images = pending_request.get("extra_images", {})
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
        site
    )


def cancel_send(site_key: str = "mulerun"):
    """Cancel the pending request"""
    return ("Request cancelled", refresh_task_table(site_key), get_stats_text(site_key),
            gr.update(visible=False, value=""), None,
            gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))
