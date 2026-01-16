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

    # Custom CSS with orange brand color
    custom_css = """
    /* Orange brand color theme */
    :root {
        --brand-orange: #f97316;
        --brand-orange-light: #fed7aa;
        --brand-orange-dark: #ea580c;
    }

    /* Title styling */
    .title-container {
        text-align: center;
        padding: 1rem 0 0.5rem 0;
        border-bottom: 3px solid var(--brand-orange);
        margin-bottom: 1rem;
    }
    .title-container h1 {
        color: var(--brand-orange-dark);
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Model badges */
    .model-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        padding: 0.5rem 0;
    }
    .model-badge {
        background: linear-gradient(135deg, var(--brand-orange), var(--brand-orange-dark));
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(249, 115, 22, 0.3);
    }

    /* Stats badges */
    .stats-container {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        align-items: center;
    }
    .stat-badge {
        padding: 0.25rem 0.6rem;
        border-radius: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .stat-pending { background: #fef3c7; color: #b45309; }
    .stat-processing { background: #dbeafe; color: #1d4ed8; }
    .stat-completed { background: #d1fae5; color: #047857; }
    .stat-failed { background: #fee2e2; color: #dc2626; }

    /* Primary button orange style */
    .primary-btn, button.primary {
        background: linear-gradient(135deg, var(--brand-orange), var(--brand-orange-dark)) !important;
        border: none !important;
    }
    .primary-btn:hover, button.primary:hover {
        background: linear-gradient(135deg, var(--brand-orange-dark), #c2410c) !important;
    }

    /* Section headers */
    .section-header {
        color: var(--brand-orange-dark);
        border-left: 4px solid var(--brand-orange);
        padding-left: 0.75rem;
        margin: 1rem 0 0.5rem 0;
    }

    /* Task history title */
    .history-title {
        color: var(--brand-orange-dark);
        border-bottom: 2px solid var(--brand-orange-light);
        padding-bottom: 0.5rem;
    }

    /* Compact table styling */
    .task-table table {
        font-size: 0.9rem;
    }
    .task-table td, .task-table th {
        padding: 0.5rem !important;
    }

    /* Accordion styling */
    .gr-accordion {
        border-color: var(--brand-orange-light) !important;
    }

    /* Input focus states */
    input:focus, textarea:focus, select:focus {
        border-color: var(--brand-orange) !important;
        box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2) !important;
    }
    """

    with gr.Blocks(title="Mule Multimodal API", theme=gr.themes.Soft(), css=custom_css) as app:
        # Beautiful title with logo
        gr.HTML("""
        <div class="title-container">
            <h1>Mule Multimodal API</h1>
        </div>
        """)

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
                    gr.Markdown("### ⚙️ Parameters", elem_classes=["section-header"])

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

                    # Veo3 specific parameters
                    last_frame = gr.Image(
                        label="Last Frame",
                        type="filepath",
                        visible=False
                    )

                    reference_images = gr.Gallery(
                        label="Reference Images",
                        show_label=True,
                        columns=3,
                        rows=1,
                        height="auto",
                        object_fit="contain",
                        interactive=True,
                        visible=False
                    )

                # Submit buttons
                with gr.Row():
                    submit_btn = gr.Button("🚀 Submit Task", variant="primary")
                    confirm_send_btn = gr.Button("✅ Confirm Send", variant="primary", visible=False)
                    cancel_send_btn = gr.Button("❌ Cancel", visible=False)

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
                task_history_title = gr.Markdown("### 📋 Task History (MuleRun)", elem_classes=["history-title"])

                task_table = gr.Dataframe(
                    headers=["ID", "Task UUID", "Status", "Model", "Prompt", "Result", "Error", "Created"],
                    datatype=["number", "str", "str", "str", "str", "str", "str", "str"],
                    value=refresh_task_table("mulerun"),
                    interactive=False,
                    wrap=True
                )

                with gr.Row():
                    refresh_btn = gr.Button("🔄 Refresh", variant="secondary")
                    stats_text = gr.HTML(get_stats_text("mulerun"))

                with gr.Row():
                    selected_task_id = gr.Number(label="Task ID", precision=0, scale=1)
                    selected_task_uuid = gr.Textbox(label="Task UUID", placeholder="e.g. 5b00bd55-...", scale=2)
                    poll_btn = gr.Button("🔍 Poll", scale=1)
                    view_detail_btn = gr.Button("👁️ Detail", scale=1)
                    delete_btn = gr.Button("🗑️ Delete", variant="stop", scale=1)

                # Task Detail
                with gr.Accordion("📊 Task Detail", open=True):
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
                audio, audio_url, prompt_extend, seed, n_images, shot_type,
                last_frame, reference_images
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
                last_frame, reference_images,
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
