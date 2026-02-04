import os
from pathlib import Path
from dataclasses import dataclass
from typing import Any

import gradio as gr

from config import API_SITES, API_PROXY
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


def _load_css() -> str:
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return ""


@dataclass
class SidebarComponents:
    site_selector: Any
    api_token: Any
    proxy_input: Any
    debug_mode: Any
    task_type: Any
    model_dropdown: Any
    prompt: Any
    negative_prompt: Any
    image: Any
    image_url: Any
    multi_images: Any
    multi_images_url: Any
    model_name: Any
    mode: Any
    aspect_ratio: Any
    duration: Any
    resolution: Any
    size: Any
    seconds: Any
    cfg_scale: Any
    video_type: Any
    audio: Any
    audio_url: Any
    prompt_extend: Any
    seed: Any
    n_images: Any
    shot_type: Any
    last_frame: Any
    last_frame_url: Any
    reference_images: Any
    reference_images_url: Any
    submit_btn: Any
    confirm_send_btn: Any
    cancel_send_btn: Any
    submit_result: Any
    debug_preview: Any
    pending_request: Any


@dataclass
class TaskPanelComponents:
    task_history_title: Any
    task_table: Any
    refresh_btn: Any
    stats_text: Any
    selected_task_id: Any
    selected_task_uuid: Any
    poll_btn: Any
    view_detail_btn: Any
    delete_btn: Any
    task_info: Any
    image_gallery: Any
    video_preview: Any
    video_urls_display: Any
    result_links: Any


def _build_header():
    gr.HTML("""
    <div class="title-container">
        <h1>Mule Multimodal Studio</h1>
        <div>
        Multiple Multimodal API of <b>Kling</b>, <b>Midjourney</b>, <b>Google Veo3</b>, <b>Nano Banana Pro</b>, <b>OpenAI Sora2</b>, <b>Alibaba Wan2.5/2.6</b>, <b>Qwen Image</b> and to generate Images and Videos
        </div>
    </div>
    """)


def _build_sidebar() -> SidebarComponents:
    site_selector = gr.Dropdown(
        label="API Site",
        choices=[
            ("MuleRun (api.mulerun.com)", "mulerun"),
            ("MuleRouter (api.mulerouter.ai)", "mulerouter")
        ],
        value="mulerun",
        interactive=True
    )

    api_token = gr.Textbox(
        label="API Token",
        placeholder="Enter your API token",
        value=API_SITES["mulerun"]["token"]
    )

    proxy_input = gr.Textbox(
        label="Proxy (可选)",
        placeholder="http://127.0.0.1:7890 或 socks5://127.0.0.1:1080",
        value=API_PROXY,
        info="留空则不使用代理"
    )

    debug_mode = gr.Checkbox(
        label="Debug Mode (Preview request before sending)",
        value=True
    )

    task_type = gr.Radio(
        label="Task Type",
        choices=[("🎬 Video Generation", "video"), ("🖼️ Image Generation", "image")],
        value="video",
        interactive=True
    )

    model_dropdown = gr.Dropdown(
        label="Select Model",
        choices=get_model_choices_by_type("video", "mulerun"),
        value=None,
        interactive=True
    )

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

        image_url = gr.Textbox(
            label="Image URL (可选，优先于上传)",
            placeholder="https://example.com/image.jpg 或 Google Drive 共享链接",
            visible=False
        )

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

        multi_images_url = gr.Textbox(
            label="Image URLs (多个URL用换行分隔，优先于上传)",
            placeholder="支持 Google Drive 共享链接，每行一个URL",
            lines=3,
            visible=False
        )

        model_name = gr.Dropdown(label="Model Version", visible=False)
        mode = gr.Dropdown(label="Mode", visible=False)
        aspect_ratio = gr.Dropdown(label="Aspect Ratio", visible=False)
        duration = gr.Dropdown(label="Duration", visible=False)
        resolution = gr.Dropdown(label="Resolution", visible=False)
        size = gr.Dropdown(label="Size", visible=False)
        seconds = gr.Dropdown(label="Seconds", visible=False)
        cfg_scale = gr.Slider(
            label="CFG Scale",
            minimum=0,
            maximum=1,
            step=0.1,
            value=0.5,
            visible=False
        )
        video_type = gr.Dropdown(label="Video Type", visible=False)
        audio = gr.Dropdown(label="Audio", visible=False)
        audio_url = gr.Textbox(
            label="Audio URL",
            placeholder="支持 Google Drive 共享链接",
            visible=False
        )
        prompt_extend = gr.Dropdown(label="Prompt Extend", visible=False)
        seed = gr.Textbox(label="Seed", visible=False)
        n_images = gr.Dropdown(label="Number of Images", visible=False)
        shot_type = gr.Dropdown(label="Shot Type", visible=False)

        last_frame = gr.Image(
            label="Last Frame",
            type="filepath",
            visible=False
        )
        last_frame_url = gr.Textbox(
            label="Last Frame URL (可选，优先于上传)",
            placeholder="支持 Google Drive 共享链接",
            visible=False
        )

        reference_images = gr.Gallery(
            label="Reference Images",
            show_label=True,
            columns=3,
            rows=2,
            height="auto",
            object_fit="contain",
            interactive=True,
            visible=False
        )
        reference_images_url = gr.Textbox(
            label="Reference Images URLs (多个URL用换行分隔，优先于上传)",
            placeholder="支持 Google Drive 共享链接，每行一个URL",
            lines=2,
            visible=False
        )

    with gr.Row():
        submit_btn = gr.Button("🚀 Submit Task", variant="primary")
        confirm_send_btn = gr.Button("✅ Confirm Send", variant="primary", visible=False)
        cancel_send_btn = gr.Button("❌ Cancel", visible=False)

    submit_result = gr.Textbox(label="Result", interactive=False)

    debug_preview = gr.Code(
        label="Request Preview (Debug)",
        language="json",
        interactive=False,
        visible=False
    )

    pending_request = gr.State(value=None)

    return SidebarComponents(
        site_selector=site_selector,
        api_token=api_token,
        proxy_input=proxy_input,
        debug_mode=debug_mode,
        task_type=task_type,
        model_dropdown=model_dropdown,
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=image,
        image_url=image_url,
        multi_images=multi_images,
        multi_images_url=multi_images_url,
        model_name=model_name,
        mode=mode,
        aspect_ratio=aspect_ratio,
        duration=duration,
        resolution=resolution,
        size=size,
        seconds=seconds,
        cfg_scale=cfg_scale,
        video_type=video_type,
        audio=audio,
        audio_url=audio_url,
        prompt_extend=prompt_extend,
        seed=seed,
        n_images=n_images,
        shot_type=shot_type,
        last_frame=last_frame,
        last_frame_url=last_frame_url,
        reference_images=reference_images,
        reference_images_url=reference_images_url,
        submit_btn=submit_btn,
        confirm_send_btn=confirm_send_btn,
        cancel_send_btn=cancel_send_btn,
        submit_result=submit_result,
        debug_preview=debug_preview,
        pending_request=pending_request,
    )


def _build_task_panel() -> TaskPanelComponents:
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

    return TaskPanelComponents(
        task_history_title=task_history_title,
        task_table=task_table,
        refresh_btn=refresh_btn,
        stats_text=stats_text,
        selected_task_id=selected_task_id,
        selected_task_uuid=selected_task_uuid,
        poll_btn=poll_btn,
        view_detail_btn=view_detail_btn,
        delete_btn=delete_btn,
        task_info=task_info,
        image_gallery=image_gallery,
        video_preview=video_preview,
        video_urls_display=video_urls_display,
        result_links=result_links,
    )


def _bind_events(sidebar: SidebarComponents, task_panel: TaskPanelComponents):
    sidebar.site_selector.change(
        fn=update_site_selection,
        inputs=[sidebar.site_selector, sidebar.task_type],
        outputs=[
            sidebar.api_token,
            sidebar.model_dropdown,
            task_panel.task_table,
            task_panel.stats_text,
            task_panel.task_history_title
        ]
    )

    sidebar.task_type.change(
        fn=update_model_dropdown,
        inputs=[sidebar.task_type, sidebar.site_selector],
        outputs=[sidebar.model_dropdown]
    )

    sidebar.model_dropdown.change(
        fn=update_param_visibility,
        inputs=[sidebar.model_dropdown],
        outputs=[
            sidebar.prompt, sidebar.negative_prompt,
            sidebar.image, sidebar.image_url,
            sidebar.multi_images, sidebar.multi_images_url,
            sidebar.model_name, sidebar.mode, sidebar.aspect_ratio, sidebar.duration,
            sidebar.resolution, sidebar.size, sidebar.seconds, sidebar.cfg_scale,
            sidebar.video_type, sidebar.audio, sidebar.audio_url, sidebar.prompt_extend,
            sidebar.seed, sidebar.n_images, sidebar.shot_type,
            sidebar.last_frame, sidebar.last_frame_url,
            sidebar.reference_images, sidebar.reference_images_url
        ]
    )

    sidebar.submit_btn.click(
        fn=submit_task,
        inputs=[
            sidebar.model_dropdown, sidebar.prompt, sidebar.negative_prompt,
            sidebar.image, sidebar.image_url, sidebar.multi_images, sidebar.multi_images_url,
            sidebar.model_name, sidebar.mode, sidebar.aspect_ratio, sidebar.duration,
            sidebar.resolution, sidebar.size, sidebar.seconds, sidebar.cfg_scale,
            sidebar.video_type, sidebar.audio, sidebar.audio_url, sidebar.prompt_extend,
            sidebar.seed, sidebar.n_images, sidebar.shot_type,
            sidebar.last_frame, sidebar.last_frame_url,
            sidebar.reference_images, sidebar.reference_images_url,
            sidebar.api_token, sidebar.debug_mode, sidebar.site_selector, sidebar.proxy_input
        ],
        outputs=[
            sidebar.submit_result, task_panel.task_table, task_panel.stats_text,
            sidebar.debug_preview, sidebar.pending_request,
            sidebar.submit_btn, sidebar.confirm_send_btn, sidebar.cancel_send_btn
        ]
    )

    sidebar.confirm_send_btn.click(
        fn=confirm_send,
        inputs=[sidebar.pending_request],
        outputs=[
            sidebar.submit_result, task_panel.task_table, task_panel.stats_text,
            sidebar.debug_preview, sidebar.pending_request,
            sidebar.submit_btn, sidebar.confirm_send_btn, sidebar.cancel_send_btn
        ]
    )

    sidebar.cancel_send_btn.click(
        fn=cancel_send,
        inputs=[sidebar.site_selector],
        outputs=[
            sidebar.submit_result, task_panel.task_table, task_panel.stats_text,
            sidebar.debug_preview, sidebar.pending_request,
            sidebar.submit_btn, sidebar.confirm_send_btn, sidebar.cancel_send_btn
        ]
    )

    task_panel.refresh_btn.click(
        fn=lambda site: (refresh_task_table(site), get_stats_text(site)),
        inputs=[sidebar.site_selector],
        outputs=[task_panel.task_table, task_panel.stats_text]
    )

    task_panel.poll_btn.click(
        fn=manual_poll,
        inputs=[
            task_panel.selected_task_id,
            task_panel.selected_task_uuid,
            sidebar.api_token,
            sidebar.site_selector,
            sidebar.proxy_input
        ],
        outputs=[sidebar.submit_result, task_panel.task_table, task_panel.stats_text]
    )

    task_panel.delete_btn.click(
        fn=delete_selected_task,
        inputs=[task_panel.selected_task_id, task_panel.selected_task_uuid, sidebar.site_selector],
        outputs=[sidebar.submit_result, task_panel.task_table, task_panel.stats_text],
        js="(task_id, task_uuid, site) => { if (!confirm('Are you sure you want to delete this task?')) { throw new Error('Cancelled'); } return [task_id, task_uuid, site]; }"
    )

    task_panel.view_detail_btn.click(
        fn=get_task_detail,
        inputs=[task_panel.selected_task_id, task_panel.selected_task_uuid],
        outputs=[
            task_panel.task_info,
            task_panel.video_preview,
            task_panel.image_gallery,
            task_panel.video_urls_display,
            task_panel.result_links
        ]
    )


def create_ui():
    custom_css = _load_css()

    with gr.Blocks(title="Mule Multimodal API", theme=gr.themes.Soft(), css=custom_css) as app:
        _build_header()

        with gr.Row():
            with gr.Column(scale=1):
                sidebar = _build_sidebar()
            with gr.Column(scale=2):
                task_panel = _build_task_panel()

        _bind_events(sidebar, task_panel)

        # 页面加载时刷新任务列表（修复刷新页面后任务不更新的问题）
        app.load(
            fn=lambda: (refresh_task_table("mulerun"), get_stats_text("mulerun")),
            outputs=[task_panel.task_table, task_panel.stats_text]
        )

    return app
