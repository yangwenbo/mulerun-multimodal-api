"""
Alibaba Wan2.5 model configurations
"""

WAN2_5_T2I_PREVIEW = {
    "name": "Wan2.5 图片生成",
    "type": "text2image",
    "post_endpoint": "/vendors/alibaba/v1/wan2/image/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2/image/generation/{task_id}",
    "result_key": "images",
    "params": {
        "model": {
            "type": "hidden",
            "required": True,
            "default": "wan2.5-t2i-preview"
        },
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (图片描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1280*1280", "1024*1024",
                "1280*720", "720*1280",
                "1280*960", "960*1280",
                "1200*800", "800*1200",
                "1344*576"
            ],
            "default": "1280*1280",
            "label": "Size (分辨率)"
        },
        "n": {
            "type": "dropdown",
            "required": False,
            "options": ["1", "2", "3", "4"],
            "default": "1",
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

WAN2_5_I2I_PREVIEW = {
    "name": "Wan2.5 图片编辑",
    "type": "image2image",
    "post_endpoint": "/vendors/alibaba/v1/wan2/image/edit",
    "get_endpoint": "/vendors/alibaba/v1/wan2/image/edit/{task_id}",
    "result_key": "images",
    "image_as_array": True,
    "multi_image": True,
    "max_images": 3,
    "params": {
        "model": {
            "type": "hidden",
            "required": True,
            "default": "wan2.5-i2i-preview"
        },
        "image": {"type": "image", "required": True, "label": "Input Images (参考图片，1-3张，JPEG/PNG/BMP/WEBP，384-5000px，≤10MB)"},
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (编辑指令，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1280*1280", "1024*1024",
                "1280*720", "720*1280",
                "1280*960", "960*1280",
                "1200*800", "800*1200"
            ],
            "default": "1280*1280",
            "label": "Size (输出分辨率)"
        },
        "n": {
            "type": "dropdown",
            "required": False,
            "options": ["1", "2", "3", "4"],
            "default": "1",
            "label": "Number of Images (生成图片数量)"
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子，0-2147483647)"}
    }
}

WAN2_5_T2V_PREVIEW = {
    "name": "Wan2.5 Text-to-Video Preview",
    "type": "text2video",
    "post_endpoint": "/vendors/alibaba/v1/wan2/video/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2/video/generation/{task_id}",
    "params": {
        "model": {
            "type": "hidden",
            "required": True,
            "default": "wan2.5-t2v-preview"
        },
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (视频内容描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1280*720", "720*1280", "960*960", "1088*832", "832*1088",
                "1920*1080", "1080*1920", "1440*1440", "1632*1248", "1248*1632",
                "832*480", "480*832", "624*624"
            ],
            "default": "1280*720",
            "label": "Size (分辨率)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10"],
            "default": "5",
            "label": "Duration (秒)"
        },
        "audio": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Audio (自动生成音频)",
            "value_map": {"true": True, "false": False}
        },
        "audio_url": {"type": "text", "required": False, "label": "Audio URL (自定义音频URL，wav/mp3，3-30秒，≤15MB)"},
        "prompt_extend": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Prompt Extend (智能提示词扩展)",
            "value_map": {"true": True, "false": False}
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子，0-2147483647)"}
    }
}

WAN2_5_I2V_PREVIEW = {
    "name": "Wan2.5 Image-to-Video Preview",
    "type": "image2video",
    "post_endpoint": "/vendors/alibaba/v1/wan2/video/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2/video/generation/{task_id}",
    "params": {
        "model": {
            "type": "hidden",
            "required": True,
            "default": "wan2.5-i2v-preview"
        },
        "image": {"type": "image", "required": True, "label": "Input Image (首帧图片，JPEG/PNG/BMP/WEBP，360-2000px，≤10MB)"},
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (运动/故事描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["480P", "720P", "1080P"],
            "default": "720P",
            "label": "Resolution (分辨率)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10"],
            "default": "5",
            "label": "Duration (秒)"
        },
        "audio": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Audio (自动生成音频)",
            "value_map": {"true": True, "false": False}
        },
        "audio_url": {"type": "text", "required": False, "label": "Audio URL (自定义音频URL，wav/mp3，3-30秒，≤15MB)"},
        "prompt_extend": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Prompt Extend (智能提示词扩展)",
            "value_map": {"true": True, "false": False}
        },
        "seed": {"type": "text", "required": False, "label": "Seed (随机种子，0-2147483647)"}
    }
}

# Export all Wan2.5 models
MODELS = {
    "wan2_5_t2i_preview": WAN2_5_T2I_PREVIEW,
    "wan2_5_i2i_preview": WAN2_5_I2I_PREVIEW,
    "wan2_5_t2v_preview": WAN2_5_T2V_PREVIEW,
    "wan2_5_i2v_preview": WAN2_5_I2V_PREVIEW,
}
