"""
Google Veo model configuration
"""

VEO3 = {
    "name": "Google Veo3",
    "type": "text2video",
    "post_endpoint": "/vendors/google/v1/veo/generation",
    "get_endpoint": "/vendors/google/v1/veo/generation/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (视频描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "image": {"type": "image", "required": False, "label": "Initial Frame (首帧图片，用于图生视频)"},
        "last_frame": {"type": "image", "required": False, "label": "Last Frame (末帧图片，与首帧配合实现插帧)"},
        "reference_images": {"type": "multi_image", "required": False, "max_images": 3, "label": "Reference Images (参考图片，仅Veo 3.1支持，最多3张)"},
        "model": {
            "type": "dropdown",
            "required": False,
            "options": ["veo-3.1", "veo-3.1-fast", "veo-3"],
            "default": "veo-3.1",
            "label": "Model (模型版本)"
        },
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["16:9", "9:16"],
            "default": "16:9",
            "label": "Aspect Ratio (宽高比)"
        },
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["720p", "1080p"],
            "default": "720p",
            "label": "Resolution (分辨率，1080p仅支持8秒)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["4", "6", "8"],
            "default": "8",
            "label": "Duration (视频时长，秒，使用reference_images时必须为8秒)"
        }
    }
}

# Export all Veo models
MODELS = {
    "veo3": VEO3,
}
