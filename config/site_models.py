"""
Site-Model configuration - which models are available for each site
"""
from .models import MODELS


# ============== Site-Model Configuration ==============
# 每个站点可以独立配置支持的模型
# 如果两个站点的同一模型有不同的endpoint，可以在这里覆盖
#
# 格式说明:
# - 简单情况: 只列出模型key，使用MODELS中定义的默认endpoint
# - 自定义endpoint: 提供dict覆盖post_endpoint和get_endpoint
#
# 示例:
#   "model_key": {}  # 使用默认endpoint
#   "model_key": {   # 覆盖endpoint
#       "post_endpoint": "/custom/path",
#       "get_endpoint": "/custom/path/{task_id}"
#   }

SITE_MODELS = {
    "mulerun": {
        # MuleRun 支持所有模型，使用默认endpoint
        "kling_text2video": {},
        "kling_image2video": {},
        "midjourney_video": {},
        "sora": {},
        "veo3": {},
        "midjourney_diffusion": {},
        "wan2_5_t2i_preview": {},
        "wan2_5_i2i_preview": {},
        "nano_banana_pro_generation": {},
        "nano_banana_pro_edit": {},
        "wan2_5_t2v_preview": {},
        "wan2_5_i2v_preview": {},
        # Wan2.6 models
        "wan2_6_t2v": {},
        "wan2_6_i2v": {},
        "wan2_6_t2i": {},
        "wan2_6_i2i": {},
        "wan2_6_t2v_spark": {},
        "wan2_6_i2v_spark": {},
        # Qwen models
        "qwen_image_max": {},
        "qwen_image_edit_plus": {},
    },
    "mulerouter": {
        # MuleRouter 支持的模型
        "nano_banana_pro_generation": {},
        "nano_banana_pro_edit": {},
        "midjourney_video": {},
        "midjourney_diffusion": {},
        "wan2_6_t2v": {},
        "wan2_6_t2v_spark": {},
        "wan2_6_i2v": {},
        "wan2_6_i2v_spark": {},
        "wan2_6_t2i": {},
        "wan2_6_i2i": {},
        "qwen_image_max": {},
        "qwen_image_edit_plus": {},
    }
}


def get_models_for_site(site_key: str) -> dict:
    """
    Get models available for a specific site.
    Returns a dict of model configs with site-specific endpoint overrides applied.
    """
    site_config = SITE_MODELS.get(site_key, {})
    result = {}

    for model_key, overrides in site_config.items():
        if model_key in MODELS:
            # 复制基础模型配置
            model_config = MODELS[model_key].copy()
            # 应用站点特定的覆盖配置
            if overrides:
                model_config.update(overrides)
            result[model_key] = model_config

    return result


def get_site_model_keys(site_key: str) -> list:
    """Get list of model keys available for a specific site"""
    return list(SITE_MODELS.get(site_key, {}).keys())
