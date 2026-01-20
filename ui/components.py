"""
UI Components - Gradio UI Builder
"""
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
    process_ai_chat_message,
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

    /* ============== AI Visual Controller Styles ============== */

    /* AI Cursor */
    #ai-cursor {
        position: fixed;
        width: 24px;
        height: 24px;
        pointer-events: none;
        z-index: 10000;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0;
    }
    #ai-cursor.visible {
        opacity: 1;
    }
    #ai-cursor svg {
        width: 100%;
        height: 100%;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }

    /* AI Element Highlight */
    .ai-highlight {
        animation: ai-highlight-pulse 0.5s ease-in-out;
        box-shadow: 0 0 0 3px var(--brand-orange), 0 0 20px rgba(249, 115, 22, 0.5) !important;
        border-radius: 4px;
    }
    @keyframes ai-highlight-pulse {
        0%, 100% { box-shadow: 0 0 0 3px var(--brand-orange), 0 0 20px rgba(249, 115, 22, 0.5); }
        50% { box-shadow: 0 0 0 5px var(--brand-orange), 0 0 30px rgba(249, 115, 22, 0.7); }
    }

    /* AI Status Overlay */
    #ai-status-overlay {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, var(--brand-orange), var(--brand-orange-dark));
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
        z-index: 10001;
        display: flex;
        align-items: center;
        gap: 8px;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
    }
    #ai-status-overlay.visible {
        opacity: 1;
        transform: translateY(0);
    }
    #ai-status-overlay .spinner {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* AI Chat Panel Styles */
    #ai_chat_panel {
        border-left: 2px solid var(--brand-orange-light);
        padding-left: 1rem;
    }
    #ai_chatbot {
        border: 1px solid var(--brand-orange-light);
        border-radius: 8px;
    }
    #ai_chat_input textarea {
        border-color: var(--brand-orange-light);
    }
    #ai_chat_input textarea:focus {
        border-color: var(--brand-orange);
    }
    """

    with gr.Blocks(title="Mule Multimodal API", theme=gr.themes.Soft(), css=custom_css) as app:
        # Beautiful title with logo
        gr.HTML("""
        <div class="title-container">
            <h1>Mule Multimodal Studio</h1>
            <div>
            Multiple Multimodal API of <b>Kling</b>, <b>Midjourney</b>, <b>Google Veo3</b>, <b>OpenAI Sora2</b>, <b>Alibaba Wan2.5/2.6</b> and <b>Google Nano Banana Pro</b> to generate Images and Videos
            </div>
            
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
                    interactive=True,
                    elem_id="ai_site_selector"
                )

                # API Token
                api_token = gr.Textbox(
                    label="API Token",
                    placeholder="Enter your API token",
                    value=API_SITES["mulerun"]["token"],
                    elem_id="ai_api_token"
                )

                # Proxy Configuration
                proxy_input = gr.Textbox(
                    label="Proxy (可选)",
                    placeholder="http://127.0.0.1:7890 或 socks5://127.0.0.1:1080",
                    value=API_PROXY,
                    info="留空则不使用代理",
                    elem_id="ai_proxy_input"
                )

                # Debug Mode
                debug_mode = gr.Checkbox(
                    label="Debug Mode (Preview request before sending)",
                    value=True,
                    elem_id="ai_debug_mode"
                )

                # Task Type Selection
                task_type = gr.Radio(
                    label="Task Type",
                    choices=[("🎬 Video Generation", "video"), ("🖼️ Image Generation", "image")],
                    value="video",
                    interactive=True,
                    elem_id="ai_task_type"
                )

                # Model Selection
                model_dropdown = gr.Dropdown(
                    label="Select Model",
                    choices=get_model_choices_by_type("video", "mulerun"),
                    value=None,
                    interactive=True,
                    elem_id="ai_model_dropdown"
                )

                # Dynamic Parameters
                with gr.Group():
                    gr.Markdown("### ⚙️ Parameters", elem_classes=["section-header"])

                    prompt = gr.Textbox(
                        label="Prompt",
                        placeholder="Enter your prompt...",
                        lines=3,
                        visible=False,
                        elem_id="ai_prompt"
                    )

                    negative_prompt = gr.Textbox(
                        label="Negative Prompt",
                        placeholder="What to avoid...",
                        lines=2,
                        visible=False,
                        elem_id="ai_negative_prompt"
                    )

                    image = gr.Image(
                        label="Input Image",
                        type="filepath",
                        visible=False,
                        elem_id="ai_image"
                    )

                    image_url = gr.Textbox(
                        label="Image URL (可选，优先于上传)",
                        placeholder="https://example.com/image.jpg 或 Google Drive 共享链接",
                        visible=False,
                        elem_id="ai_image_url"
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
                        visible=False,
                        elem_id="ai_multi_images"
                    )

                    multi_images_url = gr.Textbox(
                        label="Image URLs (多个URL用换行分隔，优先于上传)",
                        placeholder="支持 Google Drive 共享链接，每行一个URL",
                        lines=3,
                        visible=False,
                        elem_id="ai_multi_images_url"
                    )

                    model_name = gr.Dropdown(
                        label="Model Version",
                        visible=False,
                        elem_id="ai_model_name"
                    )

                    mode = gr.Dropdown(
                        label="Mode",
                        visible=False,
                        elem_id="ai_mode"
                    )

                    aspect_ratio = gr.Dropdown(
                        label="Aspect Ratio",
                        visible=False,
                        elem_id="ai_aspect_ratio"
                    )

                    duration = gr.Dropdown(
                        label="Duration",
                        visible=False,
                        elem_id="ai_duration"
                    )

                    resolution = gr.Dropdown(
                        label="Resolution",
                        visible=False,
                        elem_id="ai_resolution"
                    )

                    size = gr.Dropdown(
                        label="Size",
                        visible=False,
                        elem_id="ai_size"
                    )

                    seconds = gr.Dropdown(
                        label="Seconds",
                        visible=False,
                        elem_id="ai_seconds"
                    )

                    cfg_scale = gr.Slider(
                        label="CFG Scale",
                        minimum=0,
                        maximum=1,
                        step=0.1,
                        value=0.5,
                        visible=False,
                        elem_id="ai_cfg_scale"
                    )

                    video_type = gr.Dropdown(
                        label="Video Type",
                        visible=False,
                        elem_id="ai_video_type"
                    )

                    # Wan2.5 specific parameters
                    audio = gr.Dropdown(
                        label="Audio",
                        visible=False,
                        elem_id="ai_audio"
                    )

                    audio_url = gr.Textbox(
                        label="Audio URL",
                        placeholder="支持 Google Drive 共享链接",
                        visible=False,
                        elem_id="ai_audio_url"
                    )

                    prompt_extend = gr.Dropdown(
                        label="Prompt Extend",
                        visible=False,
                        elem_id="ai_prompt_extend"
                    )

                    seed = gr.Textbox(
                        label="Seed",
                        visible=False,
                        elem_id="ai_seed"
                    )

                    # Wan2.5 t2i specific
                    n_images = gr.Dropdown(
                        label="Number of Images",
                        visible=False,
                        elem_id="ai_n_images"
                    )

                    # Wan2.6 t2v specific
                    shot_type = gr.Dropdown(
                        label="Shot Type",
                        visible=False,
                        elem_id="ai_shot_type"
                    )

                    # Veo3 specific parameters
                    last_frame = gr.Image(
                        label="Last Frame",
                        type="filepath",
                        visible=False,
                        elem_id="ai_last_frame"
                    )

                    last_frame_url = gr.Textbox(
                        label="Last Frame URL (可选，优先于上传)",
                        placeholder="支持 Google Drive 共享链接",
                        visible=False,
                        elem_id="ai_last_frame_url"
                    )

                    reference_images = gr.Gallery(
                        label="Reference Images",
                        show_label=True,
                        columns=3,
                        rows=2,
                        height="auto",
                        object_fit="contain",
                        interactive=True,
                        visible=False,
                        elem_id="ai_reference_images"
                    )

                    reference_images_url = gr.Textbox(
                        label="Reference Images URLs (多个URL用换行分隔，优先于上传)",
                        placeholder="支持 Google Drive 共享链接，每行一个URL",
                        lines=2,
                        visible=False,
                        elem_id="ai_reference_images_url"
                    )

                # Submit buttons
                with gr.Row():
                    submit_btn = gr.Button("🚀 Submit Task", variant="primary", elem_id="ai_submit_btn")
                    confirm_send_btn = gr.Button("✅ Confirm Send", variant="primary", visible=False, elem_id="ai_confirm_send_btn")
                    cancel_send_btn = gr.Button("❌ Cancel", visible=False, elem_id="ai_cancel_send_btn")

                submit_result = gr.Textbox(label="Result", interactive=False, elem_id="ai_submit_result")

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

            # AI Chat Panel (Third Column)
            with gr.Column(scale=1, elem_id="ai_chat_panel"):
                gr.Markdown("### 🤖 AI 助手")
                ai_chatbot = gr.Chatbot(
                    elem_id="ai_chatbot",
                    height=400,
                    show_label=False
                )
                with gr.Row():
                    ai_chat_input = gr.Textbox(
                        placeholder="告诉我你想生成什么...",
                        show_label=False,
                        scale=4,
                        elem_id="ai_chat_input"
                    )
                    ai_send_btn = gr.Button("发送", variant="primary", scale=1, elem_id="ai_send_btn")

                # Hidden components for AI action handling
                ai_actions_json = gr.Textbox(visible=False, elem_id="ai_actions_json")

        # AI Visual Controller HTML elements (cursor and status overlay)
        ai_visual_html = gr.HTML("""
        <div id="ai-cursor">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 4L10.5 20.5L13 13L20.5 10.5L4 4Z" fill="#f97316" stroke="#ea580c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div id="ai-status-overlay">
            <div class="spinner"></div>
            <span id="ai-status-text"></span>
        </div>
        """)

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
                prompt, negative_prompt, image, image_url, multi_images, multi_images_url,
                model_name, mode, aspect_ratio, duration,
                resolution, size, seconds, cfg_scale, video_type,
                audio, audio_url, prompt_extend, seed, n_images, shot_type,
                last_frame, last_frame_url, reference_images, reference_images_url
            ]
        )

        # Submit task
        submit_btn.click(
            fn=submit_task,
            inputs=[
                model_dropdown, prompt, negative_prompt, image, image_url, multi_images, multi_images_url,
                model_name, mode, aspect_ratio, duration, resolution,
                size, seconds, cfg_scale, video_type,
                audio, audio_url, prompt_extend, seed, n_images, shot_type,
                last_frame, last_frame_url, reference_images, reference_images_url,
                api_token, debug_mode, site_selector, proxy_input
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
            inputs=[selected_task_id, selected_task_uuid, api_token, site_selector, proxy_input],
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

        # ============== AI Chat Event Handlers ==============

        # AI Chat submit (both button click and enter key)
        def handle_ai_chat(message, history):
            """Handle AI chat message and return streaming updates"""
            for updated_history, actions_json in process_ai_chat_message(message, history):
                yield updated_history, actions_json, ""  # Clear input after sending

        ai_send_btn.click(
            fn=handle_ai_chat,
            inputs=[ai_chat_input, ai_chatbot],
            outputs=[ai_chatbot, ai_actions_json, ai_chat_input]
        )

        ai_chat_input.submit(
            fn=handle_ai_chat,
            inputs=[ai_chat_input, ai_chatbot],
            outputs=[ai_chatbot, ai_actions_json, ai_chat_input]
        )

        # Trigger JavaScript execution when actions_json changes
        ai_actions_json.change(
            fn=lambda x: x,
            inputs=[ai_actions_json],
            outputs=[ai_actions_json],
            js="""(actionsJson) => {
                console.log('=== AI Actions Handler ===');
                console.log('Actions JSON received:', actionsJson);
                console.log('AIVisualController exists:', !!window.AIVisualController);

                if (!actionsJson || !actionsJson.trim()) {
                    console.log('Empty actions JSON, skipping');
                    return '';
                }

                if (!window.AIVisualController) {
                    console.error('AIVisualController not found! Trying to initialize...');
                    return '';
                }

                try {
                    console.log('Calling processActionsJson...');
                    window.AIVisualController.processActionsJson(actionsJson);
                    console.log('processActionsJson completed');
                } catch (e) {
                    console.error('Error calling processActionsJson:', e);
                }

                return '';
            }"""
        )

        # Initialize AIVisualController when app loads
        app.load(
            fn=lambda: None,
            inputs=None,
            outputs=None,
            js="""() => {
                console.log('=== Initializing AI Visual Controller ===');

                // Define the AIVisualController
                window.AIVisualController = {
                    cursor: null,
                    statusOverlay: null,
                    isExecuting: false,
                    actionQueue: [],

                    init() {
                        this.cursor = document.getElementById('ai-cursor');
                        this.statusOverlay = document.getElementById('ai-status-overlay');
                        this.statusText = document.getElementById('ai-status-text');
                        console.log('AI Visual Controller initialized');
                        console.log('Cursor element:', this.cursor);
                        console.log('Status overlay:', this.statusOverlay);
                    },

                    showStatus(message) {
                        if (this.statusText && this.statusOverlay) {
                            this.statusText.textContent = message;
                            this.statusOverlay.classList.add('visible');
                        }
                    },

                    hideStatus() {
                        if (this.statusOverlay) {
                            this.statusOverlay.classList.remove('visible');
                        }
                    },

                    getElement(elemId) {
                        console.log('Looking for element:', elemId);
                        let el = document.getElementById(elemId);
                        if (el) { console.log('Found by direct ID:', el); return el; }

                        el = document.querySelector('[id$="' + elemId + '"]');
                        if (el) { console.log('Found by suffix selector:', el); return el; }

                        el = document.querySelector('[data-testid="' + elemId + '"]');
                        if (el) { console.log('Found by data-testid:', el); return el; }

                        const container = document.querySelector('#' + elemId + ', [id$="' + elemId + '"]');
                        if (container) {
                            const inner = container.querySelector('input, select, textarea, button');
                            console.log('Found container, inner element:', inner || container);
                            return inner || container;
                        }

                        console.warn('Element not found:', elemId);
                        return null;
                    },

                    async moveCursorTo(element) {
                        if (!this.cursor || !element) return;
                        const rect = element.getBoundingClientRect();
                        const x = rect.left + rect.width / 2 - 12;
                        const y = rect.top + rect.height / 2 - 12;
                        this.cursor.classList.add('visible');
                        this.cursor.style.left = x + 'px';
                        this.cursor.style.top = y + 'px';
                        await this.sleep(300);
                    },

                    hideCursor() {
                        if (this.cursor) { this.cursor.classList.remove('visible'); }
                    },

                    async highlightElement(elemId, duration = 500) {
                        const el = this.getElement(elemId);
                        if (!el) { console.warn('Element not found:', elemId); return; }
                        await this.moveCursorTo(el);
                        el.classList.add('ai-highlight');
                        await this.sleep(duration);
                        el.classList.remove('ai-highlight');
                    },

                    async clickElement(elemId) {
                        console.log('Clicking element:', elemId);
                        const container = this.getElement(elemId);
                        if (!container) { console.warn('Element not found for click:', elemId); return; }
                        await this.moveCursorTo(container);
                        await this.highlightElement(elemId, 200);

                        let clickable = container.querySelector('input[type="radio"], input[type="checkbox"]');
                        if (clickable) {
                            console.log('Found radio/checkbox:', clickable);
                            clickable.click();
                            clickable.dispatchEvent(new Event('input', { bubbles: true }));
                            clickable.dispatchEvent(new Event('change', { bubbles: true }));
                        } else {
                            clickable = container.querySelector('button') || container;
                            console.log('Found button:', clickable);
                            clickable.click();
                        }
                        await this.sleep(300);
                    },

                    async selectValue(elemId, value) {
                        console.log('Selecting value:', value, 'in element:', elemId);
                        const container = this.getElement(elemId);
                        if (!container) { console.warn('Element not found for select:', elemId); return; }
                        await this.moveCursorTo(container);
                        await this.highlightElement(elemId, 200);

                        // Step 1: Click to open the dropdown
                        const input = container.querySelector('input');
                        if (input) {
                            console.log('Found dropdown input, clicking to open...');
                            input.focus();
                            input.click();
                            await this.sleep(300);

                            // Step 2: Wait for dropdown options to appear and find matching option
                            let found = false;
                            const maxAttempts = 10;
                            for (let attempt = 0; attempt < maxAttempts && !found; attempt++) {
                                // Look for dropdown options in various possible structures
                                const optionSelectors = [
                                    '[role="listbox"] [role="option"]',
                                    '[role="option"]',
                                    '.dropdown-content li',
                                    '.options li',
                                    'ul[role="listbox"] li',
                                    '.svelte-select-list .item',
                                    '[data-testid="dropdown-option"]'
                                ];

                                for (const selector of optionSelectors) {
                                    const options = document.querySelectorAll(selector);
                                    console.log('Searching with selector:', selector, 'found:', options.length);

                                    for (const opt of options) {
                                        const optText = opt.textContent || opt.innerText || '';
                                        console.log('Checking option:', optText.trim());

                                        // Match by exact value or by text containing the value
                                        if (optText.toLowerCase().includes(value.toLowerCase()) ||
                                            value.toLowerCase().includes(optText.trim().toLowerCase())) {
                                            console.log('Found matching option:', optText.trim());

                                            // Move cursor to option and click
                                            await this.moveCursorTo(opt);
                                            opt.scrollIntoView({ block: 'nearest' });
                                            await this.sleep(100);

                                            opt.click();
                                            found = true;
                                            console.log('Clicked option successfully');
                                            break;
                                        }
                                    }
                                    if (found) break;
                                }

                                if (!found) {
                                    console.log('Option not found yet, waiting... attempt:', attempt + 1);
                                    await this.sleep(200);
                                }
                            }

                            // Fallback: if still not found, try typing and pressing Enter
                            if (!found) {
                                console.log('Fallback: typing value and pressing Enter');
                                input.value = value;
                                input.dispatchEvent(new InputEvent('input', { bubbles: true, data: value }));
                                await this.sleep(200);
                                input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
                            }
                        }
                        await this.sleep(300);
                    },

                    async typeText(elemId, text, speed = 50) {
                        console.log('Typing text:', text, 'in element:', elemId);
                        const container = this.getElement(elemId);
                        if (!container) { console.warn('Element not found for type:', elemId); return; }
                        await this.moveCursorTo(container);
                        await this.highlightElement(elemId, 200);

                        const input = container.querySelector('textarea, input[type="text"], input:not([type])') || container;
                        console.log('Found input for typing:', input);
                        if (input && (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA')) {
                            input.focus();
                            input.click();
                            await this.sleep(50);
                            input.value = '';
                            input.dispatchEvent(new InputEvent('input', { bubbles: true }));
                            for (const char of text) {
                                input.value += char;
                                input.dispatchEvent(new InputEvent('input', { bubbles: true, data: char }));
                                await this.sleep(speed);
                            }
                            input.dispatchEvent(new Event('change', { bubbles: true }));
                            input.dispatchEvent(new Event('blur', { bubbles: true }));
                        }
                        await this.sleep(100);
                    },

                    async clearInput(elemId) {
                        const container = this.getElement(elemId);
                        if (!container) return;
                        const input = container.querySelector('input, textarea') || container;
                        if (input) {
                            input.focus();
                            input.value = '';
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                            input.dispatchEvent(new Event('change', { bubbles: true }));
                        }
                    },

                    sleep(ms) {
                        return new Promise(resolve => setTimeout(resolve, ms));
                    },

                    async executeAction(action) {
                        console.log('Executing action:', action);
                        const actionValue = action.value || action.text;

                        switch (action.type) {
                            case 'status':
                                this.showStatus(action.message);
                                await this.sleep(500);
                                break;
                            case 'highlight':
                                await this.highlightElement(action.target, action.duration || 500);
                                break;
                            case 'click':
                                await this.clickElement(action.target);
                                break;
                            case 'select':
                                await this.selectValue(action.target, actionValue);
                                break;
                            case 'type':
                                await this.typeText(action.target, actionValue, action.speed || 50);
                                break;
                            case 'clear':
                                await this.clearInput(action.target);
                                break;
                            case 'wait':
                                await this.sleep(action.duration || 1000);
                                break;
                            default:
                                console.warn('Unknown action type:', action.type);
                        }
                    },

                    async executeActions(actions) {
                        if (this.isExecuting) {
                            console.log('Already executing, queueing actions');
                            this.actionQueue.push(...actions);
                            return;
                        }
                        this.isExecuting = true;
                        try {
                            for (const action of actions) {
                                await this.executeAction(action);
                            }
                            while (this.actionQueue.length > 0) {
                                const nextAction = this.actionQueue.shift();
                                await this.executeAction(nextAction);
                            }
                        } finally {
                            this.isExecuting = false;
                            this.hideCursor();
                            this.hideStatus();
                        }
                    },

                    processActionsJson(jsonStr) {
                        console.log('processActionsJson called with:', jsonStr);
                        if (!jsonStr || !jsonStr.trim()) {
                            console.log('Empty JSON string, skipping');
                            return;
                        }
                        try {
                            const actions = JSON.parse(jsonStr);
                            console.log('Parsed actions:', actions);
                            if (Array.isArray(actions) && actions.length > 0) {
                                console.log('Executing', actions.length, 'actions');
                                this.executeActions(actions);
                            } else {
                                console.log('No valid actions array found');
                            }
                        } catch (e) {
                            console.error('Failed to parse actions JSON:', e, 'Input:', jsonStr);
                        }
                    }
                };

                // Initialize the controller
                window.AIVisualController.init();
                console.log('AIVisualController ready:', !!window.AIVisualController);

                return [];
            }"""
        )

    return app
