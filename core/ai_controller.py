"""
AI Visual Controller - Command Queue and Action Parser

This module manages the command queue for AI-driven visual interactions
with the Gradio UI. It provides:
- Thread-safe command queue for pending actions
- Action parsing from AI responses
- Command state management
"""

import json
import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class ActionType(Enum):
    """Types of visual actions the AI can perform"""
    STATUS = "status"          # Show status message
    HIGHLIGHT = "highlight"    # Highlight an element
    CLICK = "click"           # Click an element
    SELECT = "select"         # Select dropdown value
    TYPE = "type"             # Type text into input
    CLEAR = "clear"           # Clear input field
    CHECK = "check"           # Check/uncheck checkbox
    WAIT = "wait"             # Wait for specified time


@dataclass
class AIAction:
    """Represents a single AI action to be executed"""
    id: str
    action_type: ActionType
    target: Optional[str] = None      # elem_id of target element (e.g., "ai_prompt")
    value: Optional[Any] = None       # Value for select/type actions
    message: Optional[str] = None     # Message for status actions
    duration: int = 500               # Duration in ms for highlight/wait
    speed: int = 50                   # Typing speed in ms per character
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert action to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "type": self.action_type.value,
            "target": self.target,
            "value": self.value,
            "message": self.message,
            "duration": self.duration,
            "speed": self.speed,
        }


class AICommandQueue:
    """Thread-safe command queue for AI actions"""

    def __init__(self):
        self._queue: List[AIAction] = []
        self._lock = threading.Lock()
        self._action_history: List[AIAction] = []
        self._current_batch_id: Optional[str] = None

    def add_action(self, action: AIAction) -> str:
        """Add an action to the queue. Returns the action ID."""
        with self._lock:
            self._queue.append(action)
            return action.id

    def add_actions(self, actions: List[AIAction]) -> List[str]:
        """Add multiple actions to the queue. Returns list of action IDs."""
        with self._lock:
            for action in actions:
                self._queue.append(action)
            return [a.id for a in actions]

    def get_pending_actions(self) -> List[Dict]:
        """Get all pending actions as JSON-serializable dicts"""
        with self._lock:
            actions = [a.to_dict() for a in self._queue]
            return actions

    def pop_pending_actions(self) -> List[Dict]:
        """Get and remove all pending actions"""
        with self._lock:
            actions = [a.to_dict() for a in self._queue]
            self._action_history.extend(self._queue)
            self._queue = []
            return actions

    def clear(self):
        """Clear all pending actions"""
        with self._lock:
            self._queue = []

    def get_queue_length(self) -> int:
        """Get number of pending actions"""
        with self._lock:
            return len(self._queue)

    def start_batch(self) -> str:
        """Start a new batch of actions. Returns batch ID."""
        self._current_batch_id = str(uuid.uuid4())[:8]
        return self._current_batch_id

    def get_current_batch_id(self) -> Optional[str]:
        """Get the current batch ID"""
        return self._current_batch_id


# Global command queue instance
_command_queue: Optional[AICommandQueue] = None


def get_command_queue() -> AICommandQueue:
    """Get the global command queue instance (singleton)"""
    global _command_queue
    if _command_queue is None:
        _command_queue = AICommandQueue()
    return _command_queue


def create_action(
    action_type: str,
    target: Optional[str] = None,
    value: Optional[Any] = None,
    message: Optional[str] = None,
    duration: int = 500,
    speed: int = 50
) -> AIAction:
    """Factory function to create an AIAction"""
    return AIAction(
        id=str(uuid.uuid4())[:8],
        action_type=ActionType(action_type),
        target=target,
        value=value,
        message=message,
        duration=duration,
        speed=speed,
    )


def parse_ai_response(response: str) -> List[AIAction]:
    """
    Parse AI response to extract action sequences.

    Expected format in the response:
    ```json
    {
      "actions": [
        {"type": "status", "message": "Setting up..."},
        {"type": "highlight", "target": "ai_prompt", "duration": 500},
        {"type": "click", "target": "ai_task_type"},
        {"type": "select", "target": "ai_model_dropdown", "value": "Kling"},
        {"type": "type", "target": "ai_prompt", "text": "sunset", "speed": 50},
        {"type": "click", "target": "ai_submit_btn"}
      ]
    }
    ```

    Returns list of AIAction objects.
    """
    actions = []

    # Try to find JSON block in the response
    json_patterns = [
        r'```json\s*(\{[\s\S]*?\})\s*```',  # Markdown code block
        r'```\s*(\{[\s\S]*?\})\s*```',       # Generic code block
        r'(\{[\s\S]*"actions"[\s\S]*\})',    # Raw JSON with actions
    ]

    json_str = None
    for pattern in json_patterns:
        match = re.search(pattern, response)
        if match:
            json_str = match.group(1)
            break

    if not json_str:
        return actions

    try:
        data = json.loads(json_str)
        action_list = data.get("actions", [])

        for item in action_list:
            action_type = item.get("type")
            if not action_type:
                continue

            try:
                action = create_action(
                    action_type=action_type,
                    target=item.get("target"),
                    value=item.get("value") or item.get("text"),  # Support both "value" and "text"
                    message=item.get("message"),
                    duration=item.get("duration", 500),
                    speed=item.get("speed", 50),
                )
                actions.append(action)
            except ValueError:
                # Skip invalid action types
                continue

    except json.JSONDecodeError:
        pass

    return actions


def queue_actions_from_response(response: str) -> List[str]:
    """
    Parse AI response and add actions to the global queue.
    Returns list of queued action IDs.
    """
    actions = parse_ai_response(response)
    if not actions:
        return []

    queue = get_command_queue()
    queue.start_batch()
    return queue.add_actions(actions)


# Convenience functions for creating common action sequences

def create_status_action(message: str) -> AIAction:
    """Create a status display action"""
    return create_action("status", message=message)


def create_highlight_action(target: str, duration: int = 500) -> AIAction:
    """Create an element highlight action"""
    return create_action("highlight", target=target, duration=duration)


def create_click_action(target: str) -> AIAction:
    """Create a click action"""
    return create_action("click", target=target)


def create_select_action(target: str, value: str) -> AIAction:
    """Create a dropdown select action"""
    return create_action("select", target=target, value=value)


def create_type_action(target: str, text: str, speed: int = 50) -> AIAction:
    """Create a text typing action"""
    return create_action("type", target=target, value=text, speed=speed)


def create_clear_action(target: str) -> AIAction:
    """Create a clear input action"""
    return create_action("clear", target=target)


def create_wait_action(duration: int = 1000) -> AIAction:
    """Create a wait action"""
    return create_action("wait", duration=duration)


# Element ID mapping for reference
ELEMENT_IDS = {
    "site_selector": "ai_site_selector",
    "api_token": "ai_api_token",
    "proxy": "ai_proxy_input",
    "debug_mode": "ai_debug_mode",
    "task_type": "ai_task_type",
    "model_dropdown": "ai_model_dropdown",
    "prompt": "ai_prompt",
    "negative_prompt": "ai_negative_prompt",
    "image": "ai_image",
    "image_url": "ai_image_url",
    "multi_images": "ai_multi_images",
    "multi_images_url": "ai_multi_images_url",
    "model_name": "ai_model_name",
    "mode": "ai_mode",
    "aspect_ratio": "ai_aspect_ratio",
    "duration": "ai_duration",
    "resolution": "ai_resolution",
    "size": "ai_size",
    "seconds": "ai_seconds",
    "cfg_scale": "ai_cfg_scale",
    "video_type": "ai_video_type",
    "audio": "ai_audio",
    "audio_url": "ai_audio_url",
    "prompt_extend": "ai_prompt_extend",
    "seed": "ai_seed",
    "n_images": "ai_n_images",
    "shot_type": "ai_shot_type",
    "last_frame": "ai_last_frame",
    "last_frame_url": "ai_last_frame_url",
    "reference_images": "ai_reference_images",
    "reference_images_url": "ai_reference_images_url",
    "submit_btn": "ai_submit_btn",
    "confirm_send_btn": "ai_confirm_send_btn",
    "cancel_send_btn": "ai_cancel_send_btn",
    "submit_result": "ai_submit_result",
}


def get_system_prompt_for_ui() -> str:
    """
    Get the system prompt that describes available UI elements for AI.
    This helps the AI understand what elements it can interact with.
    """
    return f"""You are an AI assistant that can control a video/image generation UI.
You can interact with the following UI elements using their elem_id:

AVAILABLE ELEMENTS:
{json.dumps(ELEMENT_IDS, indent=2)}

AVAILABLE ACTIONS:
- status: Show a status message to the user
  {{"type": "status", "message": "Your message here"}}

- highlight: Highlight an element (orange glow effect)
  {{"type": "highlight", "target": "elem_id", "duration": 500}}

- click: Click a button or radio option
  {{"type": "click", "target": "elem_id"}}

- select: Select a value in a dropdown
  {{"type": "select", "target": "elem_id", "value": "option_value"}}

- type: Type text into an input field (with typing animation)
  {{"type": "type", "target": "elem_id", "text": "your text", "speed": 50}}

- clear: Clear an input field
  {{"type": "clear", "target": "elem_id"}}

- wait: Pause execution
  {{"type": "wait", "duration": 1000}}

When the user asks you to perform a task, respond with:
1. A friendly explanation of what you'll do
2. A JSON block containing the actions:

```json
{{
  "actions": [
    {{"type": "status", "message": "Starting task..."}},
    {{"type": "highlight", "target": "ai_task_type", "duration": 300}},
    ...
  ]
}}
```

IMPORTANT RULES:
- Always start with a "status" action to inform the user what you're doing
- Use "highlight" before interacting with an element so the user can see where you're clicking
- For text inputs, use "clear" first if needed, then "type"
- End with a friendly confirmation message

TASK TYPES:
- "video" for video generation
- "image" for image generation

COMMON MODELS:
- Kling (video): kling_t2v, kling_i2v
- Midjourney (image): midjourney
- Sora (video): sora_t2v
- Veo3 (video): veo3
- Wan2.5 (video/image): wan25_t2v, wan25_i2v, wan25_t2i
"""
