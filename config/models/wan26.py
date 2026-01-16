"""
Alibaba Wan2.6 model configurations
"""

WAN2_6_T2I = {
    "name": "Wan2.6 图片生成",
    "type": "text2image",
    "post_endpoint": "/vendors/alibaba/v1/wan2.6-t2i/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2.6-t2i/generation/{task_id}",
    "result_key": "images",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (图片描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1280*1280", "1024*1024", "768*768",
                "1280*720", "720*1280",
                "1280*960", "960*1280",
                "1440*720", "720*1440"
            ],
            "default": "1280*1280",
            "label": "Size (分辨率，768-1440px，宽高比1:4-4:1)"
        },
        "n": {
            "type": "dropdown",
            "required": False,
            "options": ["1", "2", "3", "4"],
            "default": "4",
            "label": "Number of Images (生成图片数量)"
        },
        "prompt_extend": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "false",
            "label": "Prompt Extend (智能提示词扩展)",
            "value_map": {"true": True, "false": False}
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子，0-2147483647)"}
    }
}

WAN2_6_I2I = {
    "name": "Wan2.6 图片编辑",
    "type": "image2image",
    "post_endpoint": "/vendors/alibaba/v1/wan2.6-image/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2.6-image/generation/{task_id}",
    "result_key": "images",
    "image_as_array": True,
    "multi_image": True,
    "max_images": 3,
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (编辑指令，最多2000字符)"},
        "image": {"type": "image", "required": True, "label": "Input Images (参考图片，1-3张，JPEG/PNG/BMP/WEBP，384-5000px，≤10MB)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1280*1280", "1024*1024", "768*768",
                "1280*720", "720*1280",
                "1280*960", "960*1280",
                "1440*720", "720*1440"
            ],
            "default": "1280*1280",
            "label": "Size (输出分辨率，768-1440px，宽高比1:4-4:1)"
        },
        "n": {
            "type": "dropdown",
            "required": False,
            "options": ["1", "2", "3", "4"],
            "default": "4",
            "label": "Number of Images (生成图片数量)"
        },
        "prompt_extend": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "false",
            "label": "Prompt Extend (智能提示词扩展)",
            "value_map": {"true": True, "false": False}
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子，0-2147483647)"}
    }
}

# Export all Wan2.6 models
MODELS = {
    "wan2_6_t2i": WAN2_6_T2I,
    "wan2_6_i2i": WAN2_6_I2I,
}
