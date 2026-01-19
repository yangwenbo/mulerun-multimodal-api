"""
API Client module for video generation services
"""
import base64
import requests
from typing import Optional, Tuple
from config import API_BASE_URL, API_TOKEN, API_PROXY, MODELS


class APIClient:
    """Unified API client for all video generation services"""

    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None, proxy: Optional[str] = None):
        self.token = token or API_TOKEN
        self.base_url = base_url or API_BASE_URL
        self.proxy = proxy if proxy else API_PROXY

    def _get_proxies(self) -> Optional[dict]:
        """Get proxy configuration for requests"""
        if self.proxy:
            return {
                "http": self.proxy,
                "https": self.proxy
            }
        return None

    def _get_headers(self) -> dict:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 data URI"""
        if image_path.startswith(("http://", "https://")):
            return image_path

        with open(image_path, "rb") as f:
            image_data = f.read()

        # Detect image type by magic bytes (file signature)
        # This is more reliable than file extension
        mime_type = self._detect_image_type(image_data)

        base64_data = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"

    def _detect_image_type(self, image_data: bytes) -> str:
        """Detect image MIME type from magic bytes"""
        # JPEG: starts with FF D8 FF
        if image_data[:3] == b'\xff\xd8\xff':
            return "image/jpeg"
        # PNG: starts with 89 50 4E 47 0D 0A 1A 0A
        elif image_data[:8] == b'\x89PNG\r\n\x1a\n':
            return "image/png"
        # WebP: starts with RIFF....WEBP
        elif image_data[:4] == b'RIFF' and image_data[8:12] == b'WEBP':
            return "image/webp"
        # GIF: starts with GIF87a or GIF89a
        elif image_data[:6] in (b'GIF87a', b'GIF89a'):
            return "image/gif"
        # BMP: starts with BM
        elif image_data[:2] == b'BM':
            return "image/bmp"
        else:
            # Default to JPEG if unknown
            return "image/jpeg"

    def _build_request_body(
        self,
        model_key: str,
        params: dict,
        image_paths: Optional[list] = None,
        model_config: Optional[dict] = None,
        extra_images: Optional[dict] = None
    ) -> Tuple[str, dict, dict]:
        """
        Build request URL, headers and body without sending.

        Args:
            model_key: The model identifier
            params: Request parameters
            image_paths: List of image paths (can be empty, single, or multiple)
            model_config: Optional model config (with site-specific overrides). If not provided, uses MODELS.
            extra_images: Optional dict of extra image parameters (e.g., last_frame, reference_images)

        Returns:
            Tuple of (url, headers, body)
        """
        config = model_config if model_config else MODELS.get(model_key)
        if not config:
            raise ValueError(f"Unknown model: {model_key}")

        endpoint = config["post_endpoint"]
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        # Build request body
        body = {}

        # Handle image encoding
        if image_paths:
            encoded_images = [self._encode_image(path) for path in image_paths]
            # Check if model uses "images" array instead of "image"
            if config.get("image_as_array"):
                body["images"] = encoded_images
            else:
                # Single image mode - use first image
                body["image"] = encoded_images[0] if encoded_images else None

        # Handle extra images (last_frame, reference_images)
        if extra_images:
            if "last_frame" in extra_images and extra_images["last_frame"]:
                body["last_frame"] = self._encode_image(extra_images["last_frame"])
            if "reference_images" in extra_images and extra_images["reference_images"]:
                body["reference_images"] = [self._encode_image(path) for path in extra_images["reference_images"]]

        # Add other parameters
        params_def = config.get("params", {})
        for key, value in params.items():
            if key == "image":
                continue  # Already handled
            if value is not None and value != "":
                # Check for value_map in config
                param_config = params_def.get(key, {})
                value_map = param_config.get("value_map")
                if value_map and value in value_map:
                    body[key] = value_map[value]
                elif key == "cfg_scale":
                    body[key] = float(value)
                elif key == "seed":
                    # Convert seed to integer
                    try:
                        body[key] = int(value)
                    except (ValueError, TypeError):
                        pass  # Skip invalid seed values
                elif key == "duration" or key == "n":
                    # Convert duration and n to integer
                    try:
                        body[key] = int(value)
                    except (ValueError, TypeError):
                        body[key] = value
                else:
                    body[key] = value

        return url, headers, body

    def get_request_preview(
        self,
        model_key: str,
        params: dict,
        image_paths: Optional[list] = None,
        model_config: Optional[dict] = None,
        extra_images: Optional[dict] = None
    ) -> Tuple[bool, str, dict]:
        """
        Get a preview of the request that would be sent.

        Args:
            model_key: The model identifier
            params: Request parameters
            image_paths: List of image paths
            model_config: Optional model config (with site-specific overrides)
            extra_images: Optional dict of extra image parameters

        Returns:
            Tuple of (success, error_message, request_info)
        """
        if not self.token:
            return False, "API Token not configured", {}

        config = model_config if model_config else MODELS.get(model_key)
        if not config:
            return False, f"Unknown model: {model_key}", {}

        url, headers, body = self._build_request_body(
            model_key, params, image_paths, config, extra_images
        )

        # Create a display-friendly version of body (truncate base64 images)
        display_body = {}
        for key, value in body.items():
            if isinstance(value, list):
                # Handle arrays (e.g., images array)
                display_list = []
                for item in value:
                    if isinstance(item, str) and "data:image" in item:
                        display_list.append(f"{item[:30]}... ({len(item)} chars)")
                    else:
                        display_list.append(item)
                display_body[key] = display_list
            elif isinstance(value, str) and "data:image" in value:
                # Find the base64 image part and truncate it
                idx = value.find("data:image")
                if idx > 0:
                    # Text before image (e.g., Midjourney prompt + image)
                    text_part = value[:idx]
                    image_part = value[idx:]
                    display_body[key] = f"{text_part}{image_part[:30]}... ({len(image_part)} chars)"
                else:
                    # Image only or image at start
                    display_body[key] = f"{value[:30]}... ({len(value)} chars)"
            else:
                display_body[key] = value

        # Create display-friendly headers (mask token)
        display_headers = dict(headers)
        if "Authorization" in display_headers:
            token = display_headers["Authorization"]
            if len(token) > 20:
                display_headers["Authorization"] = f"{token[:15]}...{token[-4:]}"

        request_info = {
            "method": "POST",
            "url": url,
            "headers": display_headers,
            "body": display_body
        }

        return True, "", request_info

    def submit_task(
        self,
        model_key: str,
        params: dict,
        image_paths: Optional[list] = None,
        model_config: Optional[dict] = None,
        extra_images: Optional[dict] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Submit a video generation task

        Args:
            model_key: The model identifier
            params: Request parameters
            image_paths: List of image paths (can be empty, single, or multiple)
            model_config: Optional model config (with site-specific overrides)
            extra_images: Optional dict of extra image parameters

        Returns:
            Tuple of (success, message, task_id)
        """
        if not self.token:
            return False, "API Token not configured", None

        config = model_config if model_config else MODELS.get(model_key)
        if not config:
            return False, f"Unknown model: {model_key}", None

        url, headers, body = self._build_request_body(
            model_key, params, image_paths, config, extra_images
        )

        try:
            response = requests.post(
                url,
                headers=headers,
                json=body,
                timeout=(60, 600),  # (connect_timeout, read_timeout) - increased for large image uploads
                proxies=self._get_proxies()
            )

            if response.status_code in (200, 202):
                data = response.json()
                task_info = data.get("task_info", {})
                task_id = task_info.get("id")

                if task_id:
                    return True, "Task submitted successfully", task_id
                else:
                    return False, "No task ID in response", None
            else:
                error_msg = f"API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg = error_data["error"].get("detail", error_msg)
                    elif "message" in error_data:
                        error_msg = error_data["message"]
                except Exception:
                    error_msg = response.text[:200]

                return False, error_msg, None

        except requests.exceptions.Timeout:
            return False, "Request timeout", None
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", None

    def get_task_status(
        self,
        model_key: str,
        task_id: str,
        model_config: Optional[dict] = None
    ) -> Tuple[str, Optional[list], Optional[str]]:
        """
        Get task status and results

        Args:
            model_key: The model identifier
            task_id: The API task ID
            model_config: Optional model config (with site-specific overrides)

        Returns:
            Tuple of (status, result_urls, error_message)
            status: 'pending', 'processing', 'completed', 'failed'
        """
        config = model_config if model_config else MODELS.get(model_key)
        if not config:
            return "failed", None, f"Unknown model: {model_key}"

        endpoint = config["get_endpoint"].format(task_id=task_id)
        url = f"{self.base_url}{endpoint}"

        # Get result key from config (default to "videos" for backward compatibility)
        result_key = config.get("result_key", "videos")

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=30,
                proxies=self._get_proxies()
            )

            if response.status_code in (200, 202):
                data = response.json()
                task_info = data.get("task_info", {})
                status = task_info.get("status", "pending")

                if status == "completed":
                    results = data.get(result_key, [])
                    return "completed", results, None
                elif status == "failed":
                    error = task_info.get("error", {})
                    error_msg = error.get("detail", "Unknown error")
                    return "failed", None, error_msg
                else:
                    return status, None, None
            else:
                return "failed", None, f"API error: {response.status_code}"

        except requests.exceptions.Timeout:
            return "processing", None, None  # Treat timeout as still processing
        except requests.exceptions.RequestException as e:
            return "failed", None, f"Request failed: {str(e)}"


# Global client instance
api_client = APIClient()
