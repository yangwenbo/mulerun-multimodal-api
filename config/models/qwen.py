"""
Alibaba Qwen image model configurations
"""

QWEN_IMAGE_MAX = {
    "name": "QwenImageMax-20251230 图片生成",
    "type": "text2image",
    "post_endpoint": "/vendors/alibaba/v1/qwen-image-max-2025-12-30/generation",
    "get_endpoint": "/vendors/alibaba/v1/qwen-image-max-2025-12-30/generation/{task_id}",
    "result_key": "images",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (图片描述)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1664*928",   # 16:9 (默认)
                "1472*1104",  # 4:3
                "1328*1328",  # 1:1
                "1104*1472",  # 3:4
                "928*1664",   # 9:16
            ],
            "default": "1664*928",
            "label": "Size (分辨率: 16:9/4:3/1:1/3:4/9:16)"
        },
        "prompt_extend": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "false",
            "label": "Prompt Extend (智能提示词扩展)",
            "value_map": {"true": True, "false": False}
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子)"}
    }
}

QWEN_IMAGE_EDIT_PLUS = {
    "name": "QwenImageEditPlus-20251215 图片编辑",
    "type": "image2image",
    "post_endpoint": "/vendors/alibaba/v1/qwen-image-edit-plus-2025-12-15/generation",
    "get_endpoint": "/vendors/alibaba/v1/qwen-image-edit-plus-2025-12-15/generation/{task_id}",
    "result_key": "images",
    "image_as_array": True,
    "multi_image": True,
    "max_images": 3,
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (编辑指令)"},
        "image": {"type": "image", "required": True, "label": "Input Images (参考图片，1-3张，URL或Base64)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容)"},
        "n": {
            "type": "dropdown",
            "required": False,
            "options": ["1", "2", "3", "4", "5", "6"],
            "default": "1",
            "label": "Number of Images (生成图片数量，1-6张)"
        },
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "",             # 默认：保持输入图像比例，接近1024*1024
                "1024*1024",    # 1:1
                "1536*1536",    # 1:1
                "768*1152",     # 2:3
                "1024*1536",    # 2:3
                "1152*768",     # 3:2
                "1536*1024",    # 3:2
                "960*1280",     # 3:4
                "1080*1440",    # 3:4
                "1280*960",     # 4:3
                "1440*1080",    # 4:3
                "720*1280",     # 9:16
                "1080*1920",    # 9:16
                "1280*720",     # 16:9
                "1920*1080",    # 16:9
                "1344*576",     # 21:9
                "2048*872",     # 21:9
            ],
            "default": "",
            "label": "Size (输出分辨率，留空则保持输入图像比例)"
        },
        "prompt_extend": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "false",
            "label": "Prompt Extend (智能提示词扩展)",
            "value_map": {"true": True, "false": False}
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子)"}
    }
}

# Export all Qwen models
MODELS = {
    "qwen_image_max": QWEN_IMAGE_MAX,
    "qwen_image_edit_plus": QWEN_IMAGE_EDIT_PLUS,
}
