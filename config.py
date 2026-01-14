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
            "image": {"type": "image", "required": False, "label": "Initial Frame (可选，没有图片就是文生视频，图片规格必须符合Size参数: 1280x720或720x1280)"},
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
    "midjourney_diffusion": {
        "name": "Midjourney 图片生成",
        "type": "text2image",
        "post_endpoint": "/vendors/midjourney/v1/tob/diffusion",
        "get_endpoint": "/vendors/midjourney/v1/tob/diffusion/{task_id}",
        "result_key": "images",
        "params": {
            "prompt": {"type": "text", "required": True, "max_length": 8192, "label": "Prompt (支持Midjourney格式，最多8192字符)"}
        }
    },
    "wan2_5_t2i_preview": {
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
    },
    "wan2_5_i2i_preview": {
        "name": "Wan2.5 图片编辑",
        "type": "image2image",
        "post_endpoint": "/vendors/alibaba/v1/wan2/image/edit",
        "get_endpoint": "/vendors/alibaba/v1/wan2/image/edit/{task_id}",
        "result_key": "images",
        "image_as_array": True,  # Special flag: send image as "images" array
        "multi_image": True,  # Support multiple images (1-2)
        "max_images": 2,
        "params": {
            "model": {
                "type": "hidden",
                "required": True,
                "default": "wan2.5-i2i-preview"
            },
            "image": {"type": "image", "required": True, "label": "Input Images (参考图片，最多2张，JPEG/PNG/BMP/WEBP，384-5000px，≤10MB)"},
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
    },
    "wan2_5_t2v_preview": {
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
    },
    "wan2_5_i2v_preview": {
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
}
