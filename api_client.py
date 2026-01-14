"""
API Client module for video generation services
"""
import base64
import requests
from typing import Optional, Tuple
from config import API_BASE_URL, API_TOKEN, MODELS


class APIClient:
    """Unified API client for all video generation services"""

    def __init__(self, token: Optional[str] = None):
        self.token = token or API_TOKEN
        self.base_url = API_BASE_URL

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

        # Detect image type
        if image_path.lower().endswith(".png"):
            mime_type = "image/png"
        elif image_path.lower().endswith((".jpg", ".jpeg")):
            mime_type = "image/jpeg"
        elif image_path.lower().endswith(".webp"):
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"

        base64_data = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"

    def _build_request_body(
        self,
        model_key: str,
        params: dict,
        image_path: Optional[str] = None
    ) -> Tuple[str, dict, dict]:
        """
        Build request URL, headers and body without sending.

        Returns:
            Tuple of (url, headers, body)
        """
        model_config = MODELS[model_key]
        endpoint = model_config["post_endpoint"]
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        # Build request body
        body = {}

        # Handle image encoding
        if image_path:
            encoded_image = self._encode_image(image_path)
            # For nano_banana_pro_edit, use "images" array instead of "image"
            if model_key == "nano_banana_pro_edit":
                body["images"] = [encoded_image]
            else:
                body["image"] = encoded_image

        # Add other parameters
        params_def = model_config.get("params", {})
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
                else:
                    body[key] = value

        return url, headers, body

    def get_request_preview(
        self,
        model_key: str,
        params: dict,
        image_path: Optional[str] = None
    ) -> Tuple[bool, str, dict]:
        """
        Get a preview of the request that would be sent.

        Returns:
            Tuple of (success, error_message, request_info)
        """
        if not self.token:
            return False, "API Token not configured", {}

        if model_key not in MODELS:
            return False, f"Unknown model: {model_key}", {}

        url, headers, body = self._build_request_body(
            model_key, params, image_path
        )

        # Create a display-friendly version of body (truncate base64 images)
        display_body = {}
        for key, value in body.items():
            if isinstance(value, str) and "data:image" in value:
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
        image_path: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Submit a video generation task

        Returns:
            Tuple of (success, message, task_id)
        """
        if not self.token:
            return False, "API Token not configured", None

        if model_key not in MODELS:
            return False, f"Unknown model: {model_key}", None

        url, headers, body = self._build_request_body(
            model_key, params, image_path
        )

        try:
            response = requests.post(
                url,
                headers=headers,
                json=body,
                timeout=60
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
        task_id: str
    ) -> Tuple[str, Optional[list], Optional[str]]:
        """
        Get task status and results

        Returns:
            Tuple of (status, result_urls, error_message)
            status: 'pending', 'processing', 'completed', 'failed'
        """
        if model_key not in MODELS:
            return "failed", None, f"Unknown model: {model_key}"

        model_config = MODELS[model_key]
        endpoint = model_config["get_endpoint"].format(task_id=task_id)
        url = f"{self.base_url}{endpoint}"

        # Get result key from config (default to "videos" for backward compatibility)
        result_key = model_config.get("result_key", "videos")

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=30
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
