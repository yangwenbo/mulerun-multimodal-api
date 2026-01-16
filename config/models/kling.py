"""
Kling model configurations
"""

KLING_TEXT2VIDEO = {
    "name": "Kling Text-to-Video",
    "type": "text2video",
    "post_endpoint": "/vendors/kling/v1/videos/text2video",
    "get_endpoint": "/vendors/kling/v1/videos/text2video/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2500, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {
            "type": "dropdown",
            "required": False,
            "options": ["kling-v2-1-master"],
            "default": "kling-v2-1-master",
            "label": "Model"
        },
        "mode": {
            "type": "dropdown",
            "required": False,
            "options": ["std", "pro"],
            "default": "std",
            "label": "Mode (std=经济, pro=高质量)"
        },
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["16:9", "9:16", "1:1"],
            "default": "16:9",
            "label": "Aspect Ratio"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10"],
            "default": "5",
            "label": "Duration (seconds)"
        },
        "cfg_scale": {
            "type": "slider",
            "required": False,
            "min": 0,
            "max": 1,
            "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        }
    }
}

KLING_IMAGE2VIDEO = {
    "name": "Kling Image-to-Video",
    "type": "image2video",
    "post_endpoint": "/vendors/kling/v1/videos/image2video",
    "get_endpoint": "/vendors/kling/v1/videos/image2video/{task_id}",
    "params": {
        "image": {"type": "image", "required": True, "label": "Input Image (小于10MB, 不小于300x300px)"},
        "prompt": {"type": "text", "required": True, "max_length": 2500, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {
            "type": "dropdown",
            "required": False,
            "options": ["kling-v2-1-master"],
            "default": "kling-v2-1-master",
            "label": "Model"
        },
        "mode": {
            "type": "dropdown",
            "required": False,
            "options": ["std", "pro"],
            "default": "std",
            "label": "Mode"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10"],
            "default": "5",
            "label": "Duration (seconds)"
        },
        "cfg_scale": {
            "type": "slider",
            "required": False,
            "min": 0,
            "max": 1,
            "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        }
    }
}

# Export all Kling models
MODELS = {
    "kling_text2video": KLING_TEXT2VIDEO,
    "kling_image2video": KLING_IMAGE2VIDEO,
}
