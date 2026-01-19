"""
Configuration module for the multimodal API client
"""

# Base configuration
from .base import (
    MULERUN_API_BASE_URL,
    MULERUN_API_TOKEN,
    MULEROUTER_API_BASE_URL,
    MULEROUTER_API_TOKEN,
    API_BASE_URL,
    API_TOKEN,
    API_PROXY,
    POLL_INTERVAL,
    MAX_POLL_ATTEMPTS,
    DB_PATH,
    MEDIA_DIR,
    AUTO_DOWNLOAD_MEDIA,
    DOWNLOAD_TIMEOUT,
)

# Site configuration
from .sites import API_SITES

# Model configuration
from .models import MODELS

# Site-model mapping
from .site_models import (
    SITE_MODELS,
    get_models_for_site,
    get_site_model_keys,
)

__all__ = [
    # Base
    "MULERUN_API_BASE_URL",
    "MULERUN_API_TOKEN",
    "MULEROUTER_API_BASE_URL",
    "MULEROUTER_API_TOKEN",
    "API_BASE_URL",
    "API_TOKEN",
    "API_PROXY",
    "POLL_INTERVAL",
    "MAX_POLL_ATTEMPTS",
    "DB_PATH",
    "MEDIA_DIR",
    "AUTO_DOWNLOAD_MEDIA",
    "DOWNLOAD_TIMEOUT",
    # Sites
    "API_SITES",
    # Models
    "MODELS",
    # Site-model mapping
    "SITE_MODELS",
    "get_models_for_site",
    "get_site_model_keys",
]
