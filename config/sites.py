"""
Site configuration - API sites and their settings
"""
from .base import (
    MULERUN_API_BASE_URL,
    MULERUN_API_TOKEN,
    MULEROUTER_API_BASE_URL,
    MULEROUTER_API_TOKEN,
)

# Site definitions
API_SITES = {
    "mulerun": {
        "name": "MuleRun",
        "base_url": MULERUN_API_BASE_URL,
        "token": MULERUN_API_TOKEN,
        "description": "api.mulerun.com"
    },
    "mulerouter": {
        "name": "MuleRouter",
        "base_url": MULEROUTER_API_BASE_URL,
        "token": MULEROUTER_API_TOKEN,
        "description": "api.mulerouter.ai"
    }
}
