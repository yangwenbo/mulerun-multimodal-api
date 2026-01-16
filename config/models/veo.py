"""
Google Veo model configuration
"""

VEO3 = {
    "name": "Google Veo3",
    "type": "text2video",
    "post_endpoint": "/vendors/google/v1/veo/generation",
    "get_endpoint": "/vendors/google/v1/veo/generation/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt"},
        "image": {"type": "image", "required": False, "label": "Initial Frame (可选，没有图片就是文生视频)"},
        "model": {
            "type": "dropdown",
            "required": False,
            "options": ["veo-3.1", "veo-3.1-fast", "veo-3"],
            "default": "veo-3.1",
            "label": "Model"
        },
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["16:9", "9:16"],
            "default": "16:9",
            "label": "Aspect Ratio"
        },
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["720p", "1080p"],
            "default": "720p",
            "label": "Resolution"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["8"],
            "default": "8",
            "label": "Duration (仅支持8秒)"
        }
    }
}

# Export all Veo models
MODELS = {
    "veo3": VEO3,
}
