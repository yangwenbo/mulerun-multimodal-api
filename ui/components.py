"""
UI Components - Gradio UI Builder
"""
import gradio as gr

from config import API_SITES
from ui.helpers import get_model_choices_by_type, refresh_task_table, get_stats_text
from ui.handlers import (
    update_site_selection,
    update_model_dropdown,
    update_param_visibility,
    submit_task,
    confirm_send,
    cancel_send,
    manual_poll,
    get_task_detail,
    delete_selected_task,
)


def create_ui():
    """Create the Gradio UI"""

    with gr.Blocks(title="Video/Image Generation Client", theme=gr.themes.Soft()) as app:
        gr.Markdown("# Video/Image Generation Client")
        gr.Markdown("Support: Kling, Midjourney, Sora2, Veo3, Wan2.5, Wan2.6, Nano Banana Pro")

        with gr.Row():
            with gr.Column(scale=1):
                # Site Selection
                site_selector = gr.Dropdown(
                    label="API Site",
                    choices=[
                        ("MuleRun (api.mulerun.com)", "mulerun"),
                        ("MuleRouter (api.mulerouter.ai)", "mulerouter")
                    ],
                    value="mulerun",
                    interactive=True
                )

                # API Token
                api_token = gr.Textbox(
                    label="API Token",
                    placeholder="Enter your API token",
                    value=API_SITES["mulerun"]["token"]
                )

                # Debug Mode
                debug_mode = gr.Checkbox(
                    label="Debug Mode (Preview request before sending)",
                    value=True
                )

                # Task Type Selection
                task_type = gr.Radio(
                    label="Task Type",
                    choices=[("🎬 Video Generation", "video"), ("🖼️ Image Generation", "image")],
                    value="video",
                    interactive=True
                )

                # Model Selection
                model_dropdown = gr.Dropdown(
                    label="Select Model",
                    choices=get_model_choices_by_type("video", "mulerun"),
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

                    # Multi-image upload for models that support it
                    multi_images = gr.Gallery(
                        label="Input Images (Multiple)",
                        show_label=True,
                        columns=4,
                        rows=2,
                        height="auto",
                        object_fit="contain",
                        interactive=True,
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

                    # Wan2.5 specific parameters
                    audio = gr.Dropdown(
                        label="Audio",
                        visible=False
                    )

                    audio_url = gr.Textbox(
                        label="Audio URL",
                        visible=False
                    )

                    prompt_extend = gr.Dropdown(
                        label="Prompt Extend",
                        visible=False
                    )

                    seed = gr.Textbox(
                        label="Seed",
                        visible=False
                    )

                    # Wan2.5 t2i specific
                    n_images = gr.Dropdown(
                        label="Number of Images",
                        visible=False
                    )

                    # Wan2.6 t2v specific
                    shot_type = gr.Dropdown(
                        label="Shot Type",
                        visible=False
                    )

                # Submit buttons
                with gr.Row():
                    submit_btn = gr.Button("Submit Task", variant="primary")
                    confirm_send_btn = gr.Button("Confirm Send", variant="primary", visible=False)
                    cancel_send_btn = gr.Button("Cancel", visible=False)

                submit_result = gr.Textbox(label="Result", interactive=False)

                # Debug preview area
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
                task_history_title = gr.Markdown("### Task History (MuleRun)")

                task_table = gr.Dataframe(
                    headers=["ID", "Task UUID", "Status", "Model", "Prompt", "Result", "Error", "Created"],
                    datatype=["number", "str", "str", "str", "str", "str", "str", "str"],
                    value=refresh_task_table("mulerun"),
                    interactive=False,
                    wrap=True
                )

                with gr.Row():
                    refresh_btn = gr.Button("Refresh List", variant="secondary")
                    stats_text = gr.Markdown(get_stats_text("mulerun"))

                with gr.Row():
                    selected_task_id = gr.Number(label="Task ID", precision=0)
                    selected_task_uuid = gr.Textbox(label="Task UUID", placeholder="e.g. 5b00bd55-bac9-441b-8c5c-baf56e58285d")
                    poll_btn = gr.Button("Poll Task")
                    view_detail_btn = gr.Button("View Detail")
                    delete_btn = gr.Button("Delete Task", variant="stop")

                # Task Detail
                with gr.Accordion("Task Detail", open=True):
                    task_info = gr.Markdown("")
                    with gr.Row():
                        image_gallery = gr.Gallery(
                            label="Image Results",
                            show_label=True,
                            columns=4,
                            rows=2,
                            height="auto",
                            object_fit="contain"
                        )
                    with gr.Row():
                        video_preview = gr.Video(label="Video Preview", visible=True)
                    video_urls_display = gr.Textbox(
                        label="Video URLs (click to copy)",
                        lines=3,
                        interactive=False,
                        visible=True
                    )
                    result_links = gr.Textbox(label="All Result URLs", lines=3, interactive=False)

        # ============== Event Handlers ==============

        # Site selection changes API token and model dropdown
        site_selector.change(
            fn=update_site_selection,
            inputs=[site_selector, task_type],
            outputs=[api_token, model_dropdown, task_table, stats_text, task_history_title]
        )

        # Task type changes model dropdown options
        task_type.change(
            fn=update_model_dropdown,
            inputs=[task_type, site_selector],
            outputs=[model_dropdown]
        )

        # Model selection changes parameter visibility
        model_dropdown.change(
            fn=update_param_visibility,
            inputs=[model_dropdown],
            outputs=[
                prompt, negative_prompt, image, multi_images,
                model_name, mode, aspect_ratio, duration,
                resolution, size, seconds, cfg_scale, video_type,
                audio, audio_url, prompt_extend, seed, n_images, shot_type
            ]
        )

        # Submit task
        submit_btn.click(
            fn=submit_task,
            inputs=[
                model_dropdown, prompt, negative_prompt, image, multi_images,
                model_name, mode, aspect_ratio, duration, resolution,
                size, seconds, cfg_scale, video_type,
                audio, audio_url, prompt_extend, seed, n_images, shot_type,
                api_token, debug_mode, site_selector
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
            inputs=[site_selector],
            outputs=[
                submit_result, task_table, stats_text,
                debug_preview, pending_request,
                submit_btn, confirm_send_btn, cancel_send_btn
            ]
        )

        # Refresh table
        refresh_btn.click(
            fn=lambda site: (refresh_task_table(site), get_stats_text(site)),
            inputs=[site_selector],
            outputs=[task_table, stats_text]
        )

        # Poll task
        poll_btn.click(
            fn=manual_poll,
            inputs=[selected_task_id, selected_task_uuid, api_token, site_selector],
            outputs=[submit_result, task_table, stats_text]
        )

        # Delete task with confirmation
        delete_btn.click(
            fn=delete_selected_task,
            inputs=[selected_task_id, selected_task_uuid, site_selector],
            outputs=[submit_result, task_table, stats_text],
            js="(task_id, task_uuid, site) => { if (!confirm('Are you sure you want to delete this task?')) { throw new Error('Cancelled'); } return [task_id, task_uuid, site]; }"
        )

        # View detail
        view_detail_btn.click(
            fn=get_task_detail,
            inputs=[selected_task_id, selected_task_uuid],
            outputs=[task_info, video_preview, image_gallery, video_urls_display, result_links]
        )

    return app
