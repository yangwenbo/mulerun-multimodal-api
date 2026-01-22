"""
Midjourney model configurations
"""

MIDJOURNEY_VIDEO = {
    "name": "MidJourney 视频生成",
    "type": "text2video",
    "post_endpoint": "/vendors/midjourney/v1/tob/video-diffusion",
    "get_endpoint": "/vendors/midjourney/v1/tob/video-diffusion/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 8192, "label": "Prompt (输入文字和图片URL，例如: a cat running https://example.com/image.jpg)"},
        "video_type": {
            "type": "dropdown",
            "required": False,
            "options": ["480p", "720p"],
            "default": "480p",
            "label": "Video Quality",
            "value_map": {"480p": 0, "720p": 1}
        }
    }
}

MIDJOURNEY_DIFFUSION = {
    "name": "Midjourney 图片生成",
    "type": "text2image",
    "post_endpoint": "/vendors/midjourney/v1/tob/diffusion",
    "get_endpoint": "/vendors/midjourney/v1/tob/diffusion/{task_id}",
    "result_key": "images",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 8192, "label": "Prompt (支持Midjourney格式，最多8192字符)"}
    }
}

# Export all Midjourney models
MODELS = {
    "midjourney_video": MIDJOURNEY_VIDEO,
    "midjourney_diffusion": MIDJOURNEY_DIFFUSION,
}
