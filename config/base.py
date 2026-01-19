"""
Base configuration - API settings, polling, database
"""
import os
from pathlib import Path


def _load_env():
    """Load .env file if exists"""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()

# API Configuration - MuleRun (default site)
MULERUN_API_BASE_URL = "https://api.mulerun.com"
MULERUN_API_TOKEN = os.environ.get("API_TOKEN", "")

# API Configuration - MuleRouter (alternative site)
MULEROUTER_API_BASE_URL = "https://api.mulerouter.ai"
MULEROUTER_API_TOKEN = os.environ.get("MULEROUTER_API_TOKEN", "")

# Default (for backward compatibility)
API_BASE_URL = MULERUN_API_BASE_URL
API_TOKEN = MULERUN_API_TOKEN

# Polling Configuration
POLL_INTERVAL = 30  # 轮询间隔（秒）
MAX_POLL_ATTEMPTS = 120  # 最大轮询次数（30秒 * 120 = 1小时）

# Database
DB_PATH = "video_tasks.db"

# Media Storage Configuration
MEDIA_DIR = "media"              # 本地媒体存储目录
AUTO_DOWNLOAD_MEDIA = True       # 是否自动下载媒体文件到本地
DOWNLOAD_TIMEOUT = 120           # 下载超时时间（秒）

# Proxy Configuration
# 支持 HTTP/HTTPS/SOCKS5 代理，例如:
# http://127.0.0.1:7890
# socks5://127.0.0.1:1080
API_PROXY = os.environ.get("API_PROXY", "")
