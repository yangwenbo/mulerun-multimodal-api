"""
Alibaba Wan2.6 model configurations
"""

WAN2_6_T2V = {
    "name": "Wan2.6 文生视频",
    "type": "text2video",
    "post_endpoint": "/vendors/alibaba/v1/wan2.6-t2v/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2.6-t2v/generation/{task_id}",
    "result_key": "videos",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (视频描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1280*720", "720*1280", "960*960",
                "1088*832", "832*1088",
                "1920*1080", "1080*1920", "1440*1440",
                "1632*1248", "1248*1632"
            ],
            "default": "1280*720",
            "label": "Size (分辨率)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10", "15"],
            "default": "5",
            "label": "Duration (视频时长，秒)"
        },
        "shot_type": {
            "type": "dropdown",
            "required": False,
            "options": ["single", "multi"],
            "default": "single",
            "label": "Shot Type (镜头类型: single=单镜头, multi=多镜头, 仅当Prompt Extend=true生效)"
        },
        "audio": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Audio (是否生成音频)",
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

WAN2_6_I2V = {
    "name": "Wan2.6 图生视频",
    "type": "image2video",
    "post_endpoint": "/vendors/alibaba/v1/wan2.6-i2v/generation",
    "get_endpoint": "/vendors/alibaba/v1/wan2.6-i2v/generation/{task_id}",
    "result_key": "videos",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (视频描述，最多2000字符)"},
        "image": {"type": "image", "required": True, "label": "Input Image (首帧图片，URL或Base64)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["720P", "1080P"],
            "default": "720P",
            "label": "Resolution (分辨率)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10", "15"],
            "default": "5",
            "label": "Duration (视频时长，秒)"
        },
        "shot_type": {
            "type": "dropdown",
            "required": False,
            "options": ["single", "multi"],
            "default": "single",
            "label": "Shot Type (镜头类型: single=单镜头, multi=多镜头, 仅当Prompt Extend=true生效)"
        },
        "audio": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Audio (是否生成音频)",
            "value_map": {"true": True, "false": False}
        },
        "audio_url": {"type": "text", "required": False, "label": "Audio URL (自定义音频URL，wav/mp3，3-30秒)"},
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

WAN2_6_T2V_SPARK = {
    "name": "Wan2.6 Spark 文生视频",
    "type": "text2video",
    "post_endpoint": "/vendors/mulerouter/v1/wan2.6-t2v-spark/generation",
    "get_endpoint": "/vendors/mulerouter/v1/wan2.6-t2v-spark/generation/{task_id}",
    "result_key": "videos",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (视频描述，最多2000字符)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "size": {
            "type": "dropdown",
            "required": False,
            "options": [
                "1920*1080", "1080*1920", "1440*1440",
                "1632*1248", "1248*1632"
            ],
            "default": "1920*1080",
            "label": "Size (分辨率)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10", "15"],
            "default": "5",
            "label": "Duration (视频时长，秒)"
        },
        "shot_type": {
            "type": "dropdown",
            "required": False,
            "options": ["single", "multi"],
            "default": "single",
            "label": "Shot Type (镜头类型: single=单镜头, multi=多镜头, 仅当Prompt Extend=true生效)"
        },
        "audio": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Audio (是否生成音频)",
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

WAN2_6_I2V_SPARK = {
    "name": "Wan2.6 Spark 图生视频",
    "type": "image2video",
    "post_endpoint": "/vendors/mulerouter/v1/wan2.6-i2v-spark/generation",
    "get_endpoint": "/vendors/mulerouter/v1/wan2.6-i2v-spark/generation/{task_id}",
    "result_key": "videos",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt (视频描述，最多2000字符)"},
        "image": {"type": "image", "required": True, "label": "Input Image (首帧图片，URL或Base64)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 500, "label": "Negative Prompt (不希望出现的内容，最多500字符)"},
        "resolution": {
            "type": "dropdown",
            "required": False,
            "options": ["1080P"],
            "default": "1080P",
            "label": "Resolution (分辨率)"
        },
        "duration": {
            "type": "dropdown",
            "required": False,
            "options": ["5", "10", "15"],
            "default": "5",
            "label": "Duration (视频时长，秒)"
        },
        "shot_type": {
            "type": "dropdown",
            "required": False,
            "options": ["single", "multi"],
            "default": "single",
            "label": "Shot Type (镜头类型: single=单镜头, multi=多镜头, 仅当Prompt Extend=true生效)"
        },
        "audio": {
            "type": "dropdown",
            "required": False,
            "options": ["true", "false"],
            "default": "true",
            "label": "Audio (是否生成音频)",
            "value_map": {"true": True, "false": False}
        },
        "audio_url": {"type": "text", "required": False, "label": "Audio URL (自定义音频URL，wav/mp3，3-30秒)"},
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

# Export all Wan2.6 models
MODELS = {
    "wan2_6_t2v": WAN2_6_T2V,
    "wan2_6_t2v_spark": WAN2_6_T2V_SPARK,
    "wan2_6_i2v": WAN2_6_I2V,
    "wan2_6_i2v_spark": WAN2_6_I2V_SPARK,
    "wan2_6_t2i": WAN2_6_T2I,
    "wan2_6_i2i": WAN2_6_I2I,
}
