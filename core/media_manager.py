"""
Media Manager module for downloading and managing local media files
"""
import os
import logging
import requests
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from config import MEDIA_DIR, AUTO_DOWNLOAD_MEDIA, DOWNLOAD_TIMEOUT

logger = logging.getLogger("media_manager")


class MediaManager:
    """Manages local media file storage and retrieval"""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir or MEDIA_DIR)
        self._ensure_base_dir()

    def _ensure_base_dir(self):
        """Ensure base media directory exists"""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_task_dir(self, task_id: int) -> Path:
        """Get the directory for a specific task"""
        task_dir = self.base_dir / str(task_id)
        task_dir.mkdir(parents=True, exist_ok=True)
        return task_dir

    def _get_file_extension(self, url: str, content_type: str = None) -> str:
        """Determine file extension from URL or content type"""
        # Try to get extension from URL path
        parsed = urlparse(url)
        path = parsed.path
        if '.' in path:
            ext = path.rsplit('.', 1)[-1].lower()
            # Clean up query params if attached
            if '?' in ext:
                ext = ext.split('?')[0]
            if ext in ('mp4', 'webm', 'mov', 'avi', 'mkv', 'png', 'jpg', 'jpeg', 'webp', 'gif'):
                return ext

        # Fall back to content type
        if content_type:
            content_type = content_type.lower()
            if 'video/mp4' in content_type:
                return 'mp4'
            elif 'video/webm' in content_type:
                return 'webm'
            elif 'video/quicktime' in content_type:
                return 'mov'
            elif 'image/png' in content_type:
                return 'png'
            elif 'image/jpeg' in content_type:
                return 'jpg'
            elif 'image/webp' in content_type:
                return 'webp'
            elif 'image/gif' in content_type:
                return 'gif'

        # Default based on common patterns
        return 'mp4'

    def _download_file(self, url: str, save_path: Path) -> bool:
        """Download a single file from URL"""
        try:
            response = requests.get(url, timeout=DOWNLOAD_TIMEOUT, stream=True)
            response.raise_for_status()

            # Get file extension from content type if not already determined
            if not save_path.suffix:
                content_type = response.headers.get('Content-Type', '')
                ext = self._get_file_extension(url, content_type)
                save_path = save_path.with_suffix(f'.{ext}')

            # Write file in chunks
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"Downloaded: {url} -> {save_path}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {url}: {e}")
            return False
        except IOError as e:
            logger.error(f"Failed to save file {save_path}: {e}")
            return False

    def download_media(self, task_id: int, urls: List[str], media_type: str = "video") -> List[str]:
        """
        Download media files from URLs to local storage

        Args:
            task_id: The local task ID
            urls: List of remote URLs to download
            media_type: Type of media ('video' or 'image')

        Returns:
            List of local file paths (relative to project root)
        """
        if not AUTO_DOWNLOAD_MEDIA:
            logger.info("Auto download disabled, skipping media download")
            return []

        if not urls:
            return []

        task_dir = self._get_task_dir(task_id)
        local_paths = []

        prefix = "video" if media_type == "video" else "image"

        for i, url in enumerate(urls, 1):
            # Determine extension from URL
            ext = self._get_file_extension(url)
            filename = f"{prefix}_{i}.{ext}"
            save_path = task_dir / filename

            if self._download_file(url, save_path):
                # Return relative path from project root
                local_paths.append(str(save_path))
            else:
                # If download fails, append None to indicate failure
                local_paths.append(None)

        # Filter out None values and log results
        successful = [p for p in local_paths if p]
        logger.info(f"Task {task_id}: Downloaded {len(successful)}/{len(urls)} files")

        return local_paths

    def get_media_paths(
        self,
        task_id: int,
        remote_urls: List[str],
        local_paths: Optional[List[str]],
        media_type: str = "video"
    ) -> Tuple[List[str], bool]:
        """
        Get media paths, preferring local files

        Args:
            task_id: The local task ID
            remote_urls: List of remote URLs
            local_paths: List of local paths (from database)
            media_type: Type of media ('video' or 'image')

        Returns:
            Tuple of (paths_to_use, needs_update)
            - paths_to_use: List of paths (local if available, remote otherwise)
            - needs_update: True if local_paths was updated and should be saved
        """
        if not remote_urls:
            return [], False

        # If no local paths stored, try to download
        if not local_paths:
            downloaded = self.download_media(task_id, remote_urls, media_type)
            if downloaded and any(downloaded):
                return downloaded, True
            return remote_urls, False

        # Check if all local files exist
        result_paths = []
        needs_redownload = False

        for i, (local_path, remote_url) in enumerate(zip(local_paths, remote_urls)):
            if local_path and os.path.exists(local_path):
                result_paths.append(local_path)
            else:
                # Local file missing, need to re-download
                needs_redownload = True
                result_paths.append(remote_url)

        # If some files are missing, try to re-download them
        if needs_redownload and AUTO_DOWNLOAD_MEDIA:
            logger.info(f"Task {task_id}: Some local files missing, attempting re-download")
            new_paths = []
            updated = False

            for i, (path, remote_url) in enumerate(zip(result_paths, remote_urls)):
                if path == remote_url:
                    # This was a missing file, try to download
                    task_dir = self._get_task_dir(task_id)
                    prefix = "video" if media_type == "video" else "image"
                    ext = self._get_file_extension(remote_url)
                    filename = f"{prefix}_{i+1}.{ext}"
                    save_path = task_dir / filename

                    if self._download_file(remote_url, save_path):
                        new_paths.append(str(save_path))
                        updated = True
                    else:
                        new_paths.append(remote_url)
                else:
                    new_paths.append(path)

            return new_paths, updated

        return result_paths, False

    def get_local_path(self, task_id: int, index: int = 0) -> Optional[str]:
        """Get local path for a specific media file"""
        task_dir = self._get_task_dir(task_id)
        if not task_dir.exists():
            return None

        # Look for files matching pattern
        for ext in ('mp4', 'webm', 'mov', 'png', 'jpg', 'jpeg', 'webp', 'gif'):
            for prefix in ('video', 'image'):
                path = task_dir / f"{prefix}_{index + 1}.{ext}"
                if path.exists():
                    return str(path)

        return None

    def cleanup_task_media(self, task_id: int):
        """Remove all media files for a specific task"""
        task_dir = self.base_dir / str(task_id)
        if task_dir.exists():
            import shutil
            shutil.rmtree(task_dir)
            logger.info(f"Cleaned up media for task {task_id}")

    def get_storage_stats(self) -> dict:
        """Get storage statistics"""
        total_size = 0
        file_count = 0
        task_count = 0

        if self.base_dir.exists():
            for task_dir in self.base_dir.iterdir():
                if task_dir.is_dir():
                    task_count += 1
                    for file in task_dir.iterdir():
                        if file.is_file():
                            file_count += 1
                            total_size += file.stat().st_size

        return {
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "file_count": file_count,
            "task_count": task_count
        }


# Global media manager instance
media_manager = MediaManager()
