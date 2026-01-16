"""
Background polling service for checking task status
"""
import threading
import time
import logging
from typing import Callable, Optional

from config import POLL_INTERVAL, MAX_POLL_ATTEMPTS, API_SITES, MODELS, get_models_for_site
from core.database import get_pending_tasks, update_task_status, update_task_result
from core.api_client import APIClient
from core.media_manager import media_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("poller")


class TaskPoller:
    """Background service to poll for task completion"""

    def __init__(self):
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._poll_counts: dict = {}  # task_id -> poll_count
        self._on_task_complete: Optional[Callable] = None
        self._on_task_failed: Optional[Callable] = None

    def set_callbacks(
        self,
        on_complete: Optional[Callable] = None,
        on_failed: Optional[Callable] = None
    ):
        """Set callback functions for task events"""
        self._on_task_complete = on_complete
        self._on_task_failed = on_failed

    def start(self):
        """Start the polling service"""
        if self._running:
            logger.info("Poller already running")
            return

        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()
        logger.info("Poller started")

    def stop(self):
        """Stop the polling service"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Poller stopped")

    def _poll_loop(self):
        """Main polling loop"""
        while self._running:
            try:
                self._poll_pending_tasks()
            except Exception as e:
                logger.error(f"Polling error: {e}")

            # Wait for next poll interval
            time.sleep(POLL_INTERVAL)

    def _poll_pending_tasks(self):
        """Poll all pending tasks"""
        tasks = get_pending_tasks()

        if not tasks:
            return

        logger.info(f"Polling {len(tasks)} pending tasks...")

        for task in tasks:
            local_id = task["id"]
            api_task_id = task["task_id"]
            model_key = task["model_key"]
            api_token = task.get("api_token")
            site = task.get("site", "mulerun")  # Default to mulerun for old tasks

            if not api_token:
                logger.warning(f"Task {local_id} has no API token, skipping")
                continue

            # Check poll count
            poll_key = f"{local_id}:{api_task_id}"
            poll_count = self._poll_counts.get(poll_key, 0)

            if poll_count >= MAX_POLL_ATTEMPTS:
                logger.warning(f"Task {local_id} exceeded max poll attempts")
                update_task_status(local_id, "failed", "Polling timeout - max attempts exceeded")
                del self._poll_counts[poll_key]

                if self._on_task_failed:
                    self._on_task_failed(task)
                continue

            # Get site configuration and model config
            site_config = API_SITES.get(site, API_SITES["mulerun"])
            base_url = site_config.get("base_url")
            site_models = get_models_for_site(site)
            model_config = site_models.get(model_key)

            # Poll the task with task-specific token and site base_url
            client = APIClient(api_token, base_url)
            status, videos, error = client.get_task_status(model_key, api_task_id, model_config)
            self._poll_counts[poll_key] = poll_count + 1

            logger.info(f"Task {local_id} (site={site}): status={status}")

            if status == "completed":
                # Determine media type based on model config
                model_base_config = MODELS.get(model_key, {})
                is_image_task = model_base_config.get("type") in ("text2image", "image2image")
                media_type = "image" if is_image_task else "video"

                # Download media to local storage
                local_paths = media_manager.download_media(local_id, videos or [], media_type)

                # Update database with both remote URLs and local paths
                update_task_result(local_id, videos or [], local_paths if local_paths else None)
                del self._poll_counts[poll_key]
                logger.info(f"Task {local_id} completed with {len(videos or [])} {media_type}(s), downloaded {len([p for p in local_paths if p])} files")

                if self._on_task_complete:
                    self._on_task_complete(task, videos)

            elif status == "failed":
                update_task_status(local_id, "failed", error)
                del self._poll_counts[poll_key]
                logger.warning(f"Task {local_id} failed: {error}")

                if self._on_task_failed:
                    self._on_task_failed(task, error)

            # For pending/processing, just continue polling

    def poll_single_task(self, local_id: int, model_key: str, api_task_id: str, api_token: str, site: str = "mulerun") -> tuple:
        """
        Poll a single task immediately (for manual refresh)

        Returns:
            Tuple of (status, videos, error)
        """
        # Get site configuration and model config
        site_config = API_SITES.get(site, API_SITES["mulerun"])
        base_url = site_config.get("base_url")
        site_models = get_models_for_site(site)
        model_config = site_models.get(model_key)

        client = APIClient(api_token, base_url)
        return client.get_task_status(model_key, api_task_id, model_config)


# Global poller instance
task_poller = TaskPoller()
