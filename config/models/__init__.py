"""
Model configurations aggregator
"""

from .kling import MODELS as KLING_MODELS
from .midjourney import MODELS as MIDJOURNEY_MODELS
from .sora import MODELS as SORA_MODELS
from .veo import MODELS as VEO_MODELS
from .wan import MODELS as WAN_MODELS
from .wan26 import MODELS as WAN26_MODELS
from .nano_banana import MODELS as NANO_BANANA_MODELS
from .qwen import MODELS as QWEN_MODELS

# Aggregate all models into a single dictionary
MODELS = {}
MODELS.update(KLING_MODELS)
MODELS.update(MIDJOURNEY_MODELS)
MODELS.update(SORA_MODELS)
MODELS.update(VEO_MODELS)
MODELS.update(WAN_MODELS)
MODELS.update(WAN26_MODELS)
MODELS.update(NANO_BANANA_MODELS)
MODELS.update(QWEN_MODELS)

__all__ = ["MODELS"]
