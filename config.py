"""
Video Generation Client Configuration
"""
import os
from pathlib import Path

# Load .env file if exists
def _load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

_load_env()

# API Configuration
API_BASE_URL = "https://api.mulerun.com"
API_TOKEN = os.environ.get("API_TOKEN", "")

# Polling Configuration
POLL_INTERVAL = 30  # 轮询间隔（秒）
MAX_POLL_ATTEMPTS = 120  # 最大轮询次数（30秒 * 120 = 1小时）

# Database
DB_PATH = "video_tasks.db"

# Model Definitions
MODELS = {
    "kling_text2video": {
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
    },
    "kling_image2video": {
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
    },
    "midjourney_video": {
        "name": "Midjourney Video Diffusion",
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
    },
    "sora": {
        "name": "OpenAI Sora",
        "type": "text2video",
        "post_endpoint": "/vendors/openai/v1/sora/generation",
        "get_endpoint": "/vendors/openai/v1/sora/generation/{task_id}",
        "params": {
            "prompt": {"type": "text", "required": True, "max_length": 2000, "label": "Prompt"},
            "image": {"type": "image", "required": False, "label": "Initial Frame (可选，图片规格必须符合Size参数: 1280x720或720x1280)"},
            "model": {
                "type": "dropdown",
                "required": False,
                "options": ["sora-2"],
                "default": "sora-2",
                "label": "Model"
            },
            "seconds": {
                "type": "dropdown",
                "required": False,
                "options": ["4", "8", "12"],
                "default": "8",
                "label": "Duration (seconds)"
            },
            "size": {
                "type": "dropdown",
                "required": False,
                "options": ["1280x720", "720x1280"],
                "default": "1280x720",
                "label": "Size (1280x720=横屏, 720x1280=竖屏)"
            }
        }
    },
    "veo3": {
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
    },
    "nano_banana_pro_generation": {
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
    },
    "nano_banana_pro_edit": {
        "name": "Nano Banana Pro 图片编辑",
        "type": "image2image",
        "post_endpoint": "/vendors/google/v1/nano-banana-pro/edit",
        "get_endpoint": "/vendors/google/v1/nano-banana-pro/edit/{task_id}",
        "result_key": "images",
        "params": {
            "prompt": {"type": "text", "required": True, "label": "Prompt (编辑指令)"},
            "image": {"type": "image", "required": True, "label": "Input Image (待编辑的图片)"},
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
}
