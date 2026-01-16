#!/usr/bin/env python3
"""
Video/Image Generation Client - Main Entry Point

This is the recommended entry point for running the application.
Usage: python main.py
"""
import os

# Disable Gradio analytics/telemetry before importing gradio
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

from ui.components import create_ui
from core.poller import task_poller


def main():
    """Main entry point for the application"""
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


if __name__ == "__main__":
    main()
