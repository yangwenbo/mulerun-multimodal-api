"""
Video Generation Client - Gradio UI
"""
import os
import json

# Disable Gradio analytics/telemetry before importing gradio
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

import gradio as gr
from datetime import datetime

from config import MODELS, API_TOKEN
from database import (
    create_task,
    update_task_api_id,
    update_task_status,
    update_task_result,
    get_all_tasks,
    get_task_by_id,
    get_task_by_uuid,
    delete_task,
    get_task_stats
)
from api_client import APIClient
from poller import task_poller


# ============== Helper Functions ==============

def get_model_choices():
    """Get model choices for dropdown"""
    return [(config["name"], key) for key, config in MODELS.items()]


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


def refresh_task_table():
    """Refresh the task table"""
    tasks = get_all_tasks(limit=100)
    data = [format_task_for_display(t) for t in tasks]
    return data


def get_stats_text():
    """Get statistics text"""
    stats = get_task_stats()
    return f"Pending: {stats['pending']} | Processing: {stats['processing']} | Completed: {stats['completed']} | Failed: {stats['failed']}"


# ============== API Token ==============

def save_token(token: str):
    """Save API token"""
    global api_client
    api_client = APIClient(token)
    return "Token saved (for this session)"


# ============== Task Submission ==============

def _build_params(
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
    video_type: str
) -> dict:
    """Build params dict from UI inputs"""
    model_config = MODELS.get(model_key, {})
    params_def = model_config.get("params", {})

    params = {"prompt": prompt}

    if negative_prompt:
        params["negative_prompt"] = negative_prompt
    if model_name and model_name != "default":
        if "model_name" in params_def:
            params["model_name"] = model_name
        elif "model" in params_def:
            params["model"] = model_name
    if mode:
        params["mode"] = mode
    if aspect_ratio:
        params["aspect_ratio"] = aspect_ratio
    if duration:
        params["duration"] = duration
    if resolution:
        params["resolution"] = resolution
    if size:
        params["size"] = size
    if seconds:
        params["seconds"] = seconds
    if cfg_scale is not None and "cfg_scale" in params_def:
        params["cfg_scale"] = cfg_scale
    if video_type:
        params["video_type"] = video_type

    return params


def submit_task(
    model_key: str,
    prompt: str,
    negative_prompt: str,
    image,
    model_name: str,
    mode: str,
    aspect_ratio: str,
    duration: str,
    resolution: str,
    size: str,
    seconds: str,
    cfg_scale: float,
    video_type: str,
    api_token: str,
    debug_mode: bool
):
    """Submit a video generation task (or preview in debug mode)"""
    print(f"[DEBUG] submit_task called with model_key: {model_key}")  # Debug line

    if not api_token:
        return ("Please enter API Token first", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    if not model_key:
        return ("Please select a model", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    model_config = MODELS.get(model_key)
    if not model_config:
        return (f"Unknown model: {model_key}", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    # Check required fields
    params_def = model_config["params"]
    if "prompt" in params_def and params_def["prompt"].get("required") and not prompt:
        return ("Prompt is required", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    if "image" in params_def and params_def["image"].get("required") and not image:
        return ("Image is required for this model", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    # Build params
    params = _build_params(
        model_key, prompt, negative_prompt, model_name, mode, aspect_ratio,
        duration, resolution, size, seconds, cfg_scale, video_type
    )

    image_path = image if image else None
    client = APIClient(api_token)

    # Debug mode: show preview and wait for confirmation
    if debug_mode:
        success, error, request_info = client.get_request_preview(
            model_key=model_key,
            params=params,
            image_path=image_path
        )

        if not success:
            return (f"Error: {error}", refresh_task_table(), get_stats_text(),
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
            "image_path": image_path,
            "api_token": api_token
        }

        return ("Review the request below and click 'Confirm Send' to proceed",
                refresh_task_table(), get_stats_text(),
                gr.update(visible=True, value=preview_text), pending_data,
                gr.update(visible=False), gr.update(visible=True), gr.update(visible=True))

    # Normal mode: submit directly
    return _do_submit(model_key, model_config["name"], prompt, params, image_path, api_token)


def _do_submit(model_key, model_name, prompt, params, image_path, api_token):
    """Actually submit the task to API"""
    # Create local task record first
    local_id = create_task(
        model_key=model_key,
        model_name=model_name,
        prompt=prompt,
        params=params,
        image_path=image_path,
        api_token=api_token
    )

    # Submit to API
    client = APIClient(api_token)
    success, message, api_task_id = client.submit_task(
        model_key=model_key,
        params=params,
        image_path=image_path
    )

    if success and api_task_id:
        update_task_api_id(local_id, api_task_id)
        result_msg = f"Task submitted successfully! ID: {local_id}, API Task: {api_task_id}"
    else:
        update_task_status(local_id, "failed", message)
        result_msg = f"Failed to submit: {message}"

    return (result_msg, refresh_task_table(), get_stats_text(),
            gr.update(visible=False, value=""), None,
            gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))


def confirm_send(pending_request):
    """Confirm and send the pending request"""
    if not pending_request:
        return ("No pending request", refresh_task_table(), get_stats_text(),
                gr.update(visible=False, value=""), None,
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False))

    return _do_submit(
        pending_request["model_key"],
        pending_request["model_name"],
        pending_request["prompt"],
        pending_request["params"],
        pending_request["image_path"],
        pending_request["api_token"]
    )


def cancel_send():
    """Cancel the pending request"""
    return ("Request cancelled", refresh_task_table(), get_stats_text(),
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


def manual_poll(task_id: int, task_uuid: str, api_token: str):
    """Manually poll a task"""
    if not api_token:
        return "Please enter API Token", refresh_task_table(), get_stats_text()

    task = _resolve_task(task_id, task_uuid)
    if not task:
        return "Task not found (check Task ID or Task UUID)", refresh_task_table(), get_stats_text()

    if not task["task_id"]:
        return "Task has no API task ID", refresh_task_table(), get_stats_text()

    client = APIClient(api_token)
    status, videos, error = client.get_task_status(task["model_key"], task["task_id"])

    if status == "completed":
        update_task_result(task["id"], videos or [])
        return f"Task completed! {len(videos or [])} video(s)", refresh_task_table(), get_stats_text()
    elif status == "failed":
        update_task_status(task["id"], "failed", error)
        return f"Task failed: {error}", refresh_task_table(), get_stats_text()
    else:
        return f"Task status: {status}", refresh_task_table(), get_stats_text()


def get_task_detail(task_id: int, task_uuid: str):
    """Get task details for preview"""
    task = _resolve_task(task_id, task_uuid)
    if not task:
        return "Task not found (enter Task ID or Task UUID)", None, None, ""

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

    # Get result URLs
    video_url = None
    image_url = None
    result_links = ""

    if task.get("result_urls"):
        try:
            urls = json.loads(task["result_urls"])
            result_links = "\n".join(urls)
            if urls:
                if is_image_task:
                    image_url = urls[0]
                else:
                    video_url = urls[0]
        except Exception:
            pass

    return info, video_url, image_url, result_links


def delete_selected_task(task_id: int, task_uuid: str):
    """Delete a task"""
    task = _resolve_task(task_id, task_uuid)
    if task:
        delete_task(task["id"])
        return f"Task {task['id']} deleted", refresh_task_table(), get_stats_text()
    return "No task selected (enter Task ID or Task UUID)", refresh_task_table(), get_stats_text()


# ============== UI Visibility Control ==============

def update_param_visibility(model_key: str):
    """Update parameter visibility based on selected model"""
    if not model_key or model_key not in MODELS:
        return [gr.update(visible=False)] * 12  # Updated count without last_frame

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

    # image
    if "image" in params:
        image_label = params["image"].get("label", "Input Image")
        updates.append(gr.update(visible=True, label=image_label))
    else:
        updates.append(gr.update(visible=False))

    # model_name / model
    has_model = "model_name" in params or "model" in params
    if has_model:
        model_param = params.get("model_name") or params.get("model")
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

    # resolution (veo3)
    if "resolution" in params:
        updates.append(gr.update(visible=True, choices=params["resolution"]["options"], value=params["resolution"]["default"]))
    else:
        updates.append(gr.update(visible=False))

    # size (sora)
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

    return updates


# ============== Build UI ==============

def create_ui():
    """Create the Gradio UI"""

    with gr.Blocks(title="Video/Image Generation Client", theme=gr.themes.Soft()) as app:
        gr.Markdown("# Video/Image Generation Client")
        gr.Markdown("Support: Kling, Midjourney Video, Sora, Veo3, Nano Banana Pro")

        with gr.Row():
            with gr.Column(scale=1):
                # API Token
                api_token = gr.Textbox(
                    label="API Token",
                    placeholder="Enter your MuleRun API token",
                    value=API_TOKEN
                )

                # Debug Mode
                debug_mode = gr.Checkbox(
                    label="Debug Mode (Preview request before sending)",
                    value=True
                )

                # Model Selection
                model_dropdown = gr.Dropdown(
                    label="Select Model",
                    choices=get_model_choices(),
                    value=None,
                    interactive=True
                )

                # Dynamic Parameters
                with gr.Group():
                    gr.Markdown("### Parameters")

                    prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="Enter your prompt...",
                        lines=3,
                        visible=False
                    )

                    negative_prompt = gr.Textbox(
                        label="Negative Prompt",
                        placeholder="What to avoid...",
                        lines=2,
                        visible=False
                    )

                    image = gr.Image(
                        label="Input Image",
                        type="filepath",
                        visible=False
                    )

                    model_name = gr.Dropdown(
                        label="Model Version",
                        visible=False
                    )

                    mode = gr.Dropdown(
                        label="Mode",
                        visible=False
                    )

                    aspect_ratio = gr.Dropdown(
                        label="Aspect Ratio",
                        visible=False
                    )

                    duration = gr.Dropdown(
                        label="Duration",
                        visible=False
                    )

                    resolution = gr.Dropdown(
                        label="Resolution",
                        visible=False
                    )

                    size = gr.Dropdown(
                        label="Size",
                        visible=False
                    )

                    seconds = gr.Dropdown(
                        label="Seconds",
                        visible=False
                    )

                    cfg_scale = gr.Slider(
                        label="CFG Scale",
                        minimum=0,
                        maximum=1,
                        step=0.1,
                        value=0.5,
                        visible=False
                    )

                    video_type = gr.Dropdown(
                        label="Video Type",
                        visible=False
                    )

                # Submit buttons
                with gr.Row():
                    submit_btn = gr.Button("Submit Task", variant="primary")
                    confirm_send_btn = gr.Button("Confirm Send", variant="primary", visible=False)
                    cancel_send_btn = gr.Button("Cancel", visible=False)

                submit_result = gr.Textbox(label="Result", interactive=False)

                # Debug preview area (without Accordion to avoid caching issues)
                debug_preview = gr.Code(
                    label="Request Preview (Debug)",
                    language="json",
                    interactive=False,
                    visible=False
                )

                # State to store pending request data
                pending_request = gr.State(value=None)

            with gr.Column(scale=2):
                # Task History
                gr.Markdown("### Task History")

                task_table = gr.Dataframe(
                    headers=["ID", "Status", "Model", "Prompt", "Result", "Error", "Created"],
                    datatype=["number", "str", "str", "str", "str", "str", "str"],
                    value=refresh_task_table(),
                    interactive=False,
                    wrap=True
                )

                with gr.Row():
                    refresh_btn = gr.Button("Refresh List", variant="secondary")
                    stats_text = gr.Markdown(get_stats_text())

                with gr.Row():
                    selected_task_id = gr.Number(label="Task ID", precision=0)
                    selected_task_uuid = gr.Textbox(label="Task UUID", placeholder="e.g. 5b00bd55-bac9-441b-8c5c-baf56e58285d")
                    poll_btn = gr.Button("Poll Task")
                    view_detail_btn = gr.Button("View Detail")
                    delete_btn = gr.Button("Delete Task", variant="stop")

                # Task Detail
                with gr.Accordion("Task Detail", open=False):
                    task_info = gr.Markdown("")
                    with gr.Row():
                        video_preview = gr.Video(label="Video Preview", visible=True)
                        image_preview = gr.Image(label="Image Preview", visible=True)
                    result_links = gr.Textbox(label="Result URLs", lines=3, interactive=False)

        # ============== Event Handlers ==============

        # Model selection changes parameter visibility
        model_dropdown.change(
            fn=update_param_visibility,
            inputs=[model_dropdown],
            outputs=[
                prompt, negative_prompt, image,
                model_name, mode, aspect_ratio, duration,
                resolution, size, seconds, cfg_scale, video_type
            ]
        )

        # Submit task
        submit_btn.click(
            fn=submit_task,
            inputs=[
                model_dropdown, prompt, negative_prompt, image,
                model_name, mode, aspect_ratio, duration, resolution,
                size, seconds, cfg_scale, video_type,
                api_token, debug_mode
            ],
            outputs=[
                submit_result, task_table, stats_text,
                debug_preview, pending_request,
                submit_btn, confirm_send_btn, cancel_send_btn
            ]
        )

        # Confirm send (debug mode)
        confirm_send_btn.click(
            fn=confirm_send,
            inputs=[pending_request],
            outputs=[
                submit_result, task_table, stats_text,
                debug_preview, pending_request,
                submit_btn, confirm_send_btn, cancel_send_btn
            ]
        )

        # Cancel send (debug mode)
        cancel_send_btn.click(
            fn=cancel_send,
            outputs=[
                submit_result, task_table, stats_text,
                debug_preview, pending_request,
                submit_btn, confirm_send_btn, cancel_send_btn
            ]
        )

        # Refresh table
        refresh_btn.click(
            fn=lambda: (refresh_task_table(), get_stats_text()),
            outputs=[task_table, stats_text]
        )

        # Poll task
        poll_btn.click(
            fn=manual_poll,
            inputs=[selected_task_id, selected_task_uuid, api_token],
            outputs=[submit_result, task_table, stats_text]
        )

        # Delete task with confirmation
        delete_btn.click(
            fn=delete_selected_task,
            inputs=[selected_task_id, selected_task_uuid],
            outputs=[submit_result, task_table, stats_text],
            js="(task_id, task_uuid) => { if (!confirm('Are you sure you want to delete this task?')) { throw new Error('Cancelled'); } return [task_id, task_uuid]; }"
        )

        # View detail
        view_detail_btn.click(
            fn=get_task_detail,
            inputs=[selected_task_id, selected_task_uuid],
            outputs=[task_info, video_preview, image_preview, result_links]
        )

    return app


# ============== Main ==============

if __name__ == "__main__":
    # Start background poller
    task_poller.start()

    # Launch UI
    app = create_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )
