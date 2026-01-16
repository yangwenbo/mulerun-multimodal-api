"""
OpenAI Sora model configuration
"""

SORA = {
    "name": "OpenAI Sora",
    "type": "text2video",
    "post_endpoint": "/vendors/openai/v1/sora/generation",
    "get_endpoint": "/vendors/openai/v1/sora/generation/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt"},
        "image": {"type": "image", "required": False, "label": "Initial Frame (可选，没有图片就是文生视频，图片规格必须符合Size参数: 1280x720或720x1280)"},
        "model": {
            "type": "dropdown",
            "required": False,
            "options": ["sora-2"],
            "default": "sora-2",
            "label": "Model"
        },
        "seconds": {
            "type": "dropdown",
            "required": False,
            "options": ["4", "8", "12"],
            "default": "8",
            "label": "Duration (seconds)"
        },
        "size": {
            "type": "dropdown",
            "required": False,
            "options": ["1280x720", "720x1280"],
            "default": "1280x720",
            "label": "Size (1280x720=横屏, 720x1280=竖屏)"
        }
    }
}

# Export all Sora models
MODELS = {
    "sora": SORA,
}
