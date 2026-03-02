"""
Nano Banana model configurations
"""

NANO_BANANA_PRO_GENERATION = {
    "name": "Nano Banana Pro 图片生成",
    "type": "text2image",
    "post_endpoint": "/vendors/google/v1/nano-banana-pro/generation",
    "get_endpoint": "/vendors/google/v1/nano-banana-pro/generation/{task_id}",
    "result_key": "images",
    "params": {
        "prompt": {"type": "text", "required": True, "label": "Prompt (图片描述)"},
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
            "default": "1:1",
            "label": "Aspect Ratio"
        },
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["1K", "2K"],
            "default": "2K",
            "label": "Resolution"
        }
    }
}

NANO_BANANA_PRO_EDIT = {
    "name": "Nano Banana Pro 图片编辑",
    "type": "image2image",
    "post_endpoint": "/vendors/google/v1/nano-banana-pro/edit",
    "get_endpoint": "/vendors/google/v1/nano-banana-pro/edit/{task_id}",
    "result_key": "images",
    "image_as_array": True,
    "multi_image": True,  # Support multiple images (1-10)
    "max_images": 10,
    "params": {
        "prompt": {"type": "text", "required": True, "label": "Prompt (编辑指令)"},
        "image": {"type": "image", "required": True, "label": "Input Images (待编辑的图片，最多10张)"},
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
            "default": "1:1",
            "label": "Aspect Ratio"
        },
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["1K", "2K"],
            "default": "2K",
            "label": "Resolution"
        }
    }
}

NANO_BANANA_2_GENERATION = {
    "name": "Nano Banana 2 图片生成",
    "type": "text2image",
    "post_endpoint": "/vendors/google/v1/nano-banana-2/generation",
    "get_endpoint": "/vendors/google/v1/nano-banana-2/generation/{task_id}",
    "result_key": "images",
    "params": {
        "prompt": {"type": "text", "required": True, "label": "Prompt (图片描述)"},
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"],
            "default": "1:1",
            "label": "Aspect Ratio"
        },
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["1K", "2K", "4K"],
            "default": "1K",
            "label": "Resolution"
        },
        "web_search": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "false",
            "label": "Web Search (Google Search grounding)",
            "value_map": {"true": True, "false": False}
        }
    }
}

NANO_BANANA_2_EDIT = {
    "name": "Nano Banana 2 图片编辑",
    "type": "image2image",
    "post_endpoint": "/vendors/google/v1/nano-banana-2/edit",
    "get_endpoint": "/vendors/google/v1/nano-banana-2/edit/{task_id}",
    "result_key": "images",
    "image_as_array": True,
    "multi_image": True,
    "max_images": 14,
    "params": {
        "prompt": {"type": "text", "required": True, "label": "Prompt (编辑指令)"},
        "image": {"type": "image", "required": True, "label": "Input Images (待编辑的图片，最多14张)"},
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["1:1", "1:4", "1:8", "2:3", "3:2", "3:4", "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"],
            "default": "1:1",
            "label": "Aspect Ratio"
        },
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["1K", "2K", "4K"],
            "default": "1K",
            "label": "Resolution"
        },
        "web_search": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "false",
            "label": "Web Search (Google Search grounding)",
            "value_map": {"true": True, "false": False}
        }
    }
}

# Export all Nano Banana models
MODELS = {
    "nano_banana_pro_generation": NANO_BANANA_PRO_GENERATION,
    "nano_banana_pro_edit": NANO_BANANA_PRO_EDIT,
    "nano_banana_2_generation": NANO_BANANA_2_GENERATION,
    "nano_banana_2_edit": NANO_BANANA_2_EDIT,
}
