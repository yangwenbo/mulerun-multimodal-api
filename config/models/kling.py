"""
Kling model configurations
Based on mule-router server implementation

Routes (new format):
- POST /v1/kling-v2.5-turbo/text-to-video/generation
- POST /v1/kling-v2.6/text-to-video/generation
- POST /v1/kling-v3/text-to-video/generation
- POST /v1/kling-v2.5-turbo/image-to-video/generation
- POST /v1/kling-v2.6/image-to-video/generation
- POST /v1/kling-v3/image-to-video/generation

Models:
- kling-v2.5-turbo: V2.5 Turbo (fast generation), sound not supported
- kling-v2.6: V2.6, sound supported (pro mode only)
- kling-v3: V3 (newest, 3-15s duration), sound supported, multi-shot supported

Sound constraints (from server payload.py):
- V2.6: sound="on" requires mode="pro" (std mode does NOT support sound="on")
- V3: sound supported in both modes
"""

_SOUND_PARAM = {
    "type": "dropdown",
    "required": False,
    "options": ["off", "on"],
    "default": "off",
    "label": "Sound (生成音频)"
}

_SOUND_PARAM_V26 = {
    "type": "dropdown",
    "required": False,
    "options": ["off", "on"],
    "default": "off",
    "label": "Sound (生成音频, on 需选 pro 模式)"
}

KLING_TEXT2VIDEO_V25_TURBO = {
    "name": "Kling v2.5 Turbo 文生视频",
    "type": "text2video",
    "post_endpoint": "/vendors/klingai/v1/kling-v2.5-turbo/text-to-video/generation",
    "get_endpoint": "/vendors/klingai/v1/kling-v2.5-turbo/text-to-video/generation/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2500, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {"type": "hidden", "default": "kling-v2-5-turbo"},
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
            "min": 0, "max": 1, "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        }
    }
}

KLING_TEXT2VIDEO_V26 = {
    "name": "Kling v2.6 文生视频",
    "type": "text2video",
    "post_endpoint": "/vendors/klingai/v1/kling-v2.6/text-to-video/generation",
    "get_endpoint": "/vendors/klingai/v1/kling-v2.6/text-to-video/generation/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": True, "max_length": 2500, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {"type": "hidden", "default": "kling-v2-6"},
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
            "min": 0, "max": 1, "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        },
        "sound": _SOUND_PARAM_V26
    }
}

KLING_TEXT2VIDEO_V3 = {
    "name": "Kling v3 文生视频",
    "type": "text2video",
    "post_endpoint": "/vendors/klingai/v1/kling-v3/text-to-video/generation",
    "get_endpoint": "/vendors/klingai/v1/kling-v3/text-to-video/generation/{task_id}",
    "params": {
        "prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Prompt (单镜头, 与多镜头二选一)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {"type": "hidden", "default": "kling-v3"},
        "mode": {
            "type": "dropdown",
            "required": False,
            "options": ["std", "pro"],
            "default": "std",
            "label": "Mode (std=经济, pro=高质量)"
        },
        "multi_shot": {
            "type": "dropdown",
            "required": False,
            "options": ["false", "true"],
            "default": "false",
            "label": "Multi Shot (多镜头模式)"
        },
        "shot_type": {
            "type": "dropdown",
            "required": False,
            "options": ["customize", "intelligence"],
            "default": "customize",
            "label": "Shot Type (multi_shot=true 时生效)"
        },
        "aspect_ratio": {
            "type": "dropdown",
            "required": False,
            "options": ["16:9", "9:16", "1:1"],
            "default": "16:9",
            "label": "Aspect Ratio"
        },
        "duration_int": {
            "type": "number",
            "required": False,
            "min": 3, "max": 15,
            "default": 5,
            "label": "Duration (3-15 seconds)"
        },
        "cfg_scale": {
            "type": "slider",
            "required": False,
            "min": 0, "max": 1, "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        },
        "sound": _SOUND_PARAM
    }
}

KLING_IMAGE2VIDEO_V25_TURBO = {
    "name": "Kling v2.5 Turbo 图生视频",
    "type": "image2video",
    "post_endpoint": "/vendors/klingai/v1/kling-v2.5-turbo/image-to-video/generation",
    "get_endpoint": "/vendors/klingai/v1/kling-v2.5-turbo/image-to-video/generation/{task_id}",
    "params": {
        "image": {"type": "image", "required": True, "label": "Input Image (小于10MB, 不小于300x300px)"},
        "last_frame": {"type": "image", "required": False, "label": "End Frame Image (可选)"},
        "prompt": {"type": "text", "required": True, "max_length": 2500, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {"type": "hidden", "default": "kling-v2-5-turbo"},
        "mode": {
            "type": "dropdown",
            "required": False,
            "options": ["std", "pro"],
            "default": "std",
            "label": "Mode (std=经济, pro=高质量)"
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
            "min": 0, "max": 1, "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        }
    }
}

KLING_IMAGE2VIDEO_V26 = {
    "name": "Kling v2.6 图生视频",
    "type": "image2video",
    "post_endpoint": "/vendors/klingai/v1/kling-v2.6/image-to-video/generation",
    "get_endpoint": "/vendors/klingai/v1/kling-v2.6/image-to-video/generation/{task_id}",
    "params": {
        "image": {"type": "image", "required": True, "label": "Input Image (小于10MB, 不小于300x300px)"},
        "last_frame": {"type": "image", "required": False, "label": "End Frame Image (可选)"},
        "prompt": {"type": "text", "required": True, "max_length": 2500, "label": "Prompt"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {"type": "hidden", "default": "kling-v2-6"},
        "mode": {
            "type": "dropdown",
            "required": False,
            "options": ["std", "pro"],
            "default": "std",
            "label": "Mode (std=经济, pro=高质量)"
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
            "min": 0, "max": 1, "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        },
        "sound": _SOUND_PARAM_V26
    }
}

KLING_IMAGE2VIDEO_V3 = {
    "name": "Kling v3 图生视频",
    "type": "image2video",
    "post_endpoint": "/vendors/klingai/v1/kling-v3/image-to-video/generation",
    "get_endpoint": "/vendors/klingai/v1/kling-v3/image-to-video/generation/{task_id}",
    "params": {
        "image": {"type": "image", "required": True, "label": "Input Image (小于10MB, 不小于300x300px)"},
        "last_frame": {"type": "image", "required": False, "label": "End Frame Image (可选)"},
        "prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Prompt (单镜头, 与多镜头二选一)"},
        "negative_prompt": {"type": "text", "required": False, "max_length": 2500, "label": "Negative Prompt"},
        "model_name": {"type": "hidden", "default": "kling-v3"},
        "mode": {
            "type": "dropdown",
            "required": False,
            "options": ["std", "pro"],
            "default": "std",
            "label": "Mode (std=经济, pro=高质量)"
        },
        "multi_shot": {
            "type": "dropdown",
            "required": False,
            "options": ["false", "true"],
            "default": "false",
            "label": "Multi Shot (多镜头模式)"
        },
        "shot_type": {
            "type": "dropdown",
            "required": False,
            "options": ["customize", "intelligence"],
            "default": "customize",
            "label": "Shot Type (multi_shot=true 时生效)"
        },
        "duration_int": {
            "type": "number",
            "required": False,
            "min": 3, "max": 15,
            "default": 5,
            "label": "Duration (3-15 seconds)"
        },
        "cfg_scale": {
            "type": "slider",
            "required": False,
            "min": 0, "max": 1, "step": 0.1,
            "default": 0.5,
            "label": "CFG Scale"
        },
        "sound": _SOUND_PARAM
    }
}

MODELS = {
    "kling_text2video_v25_turbo": KLING_TEXT2VIDEO_V25_TURBO,
    "kling_text2video_v26": KLING_TEXT2VIDEO_V26,
    "kling_text2video_v3": KLING_TEXT2VIDEO_V3,
    "kling_image2video_v25_turbo": KLING_IMAGE2VIDEO_V25_TURBO,
    "kling_image2video_v26": KLING_IMAGE2VIDEO_V26,
    "kling_image2video_v3": KLING_IMAGE2VIDEO_V3,
}
