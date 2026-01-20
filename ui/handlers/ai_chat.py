"""
AI Chat Handler - Process chat messages and generate UI actions

This module handles:
- Processing user chat messages
- Calling Claude API for response generation
- Parsing AI responses for visual actions
- Managing chat history
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, List, Tuple, Optional, Generator

from core.ai_controller import get_system_prompt_for_ui

# Try to import anthropic, handle if not installed
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None  # type: ignore


def get_anthropic_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> Any:
    """
    Get Anthropic client instance.

    Args:
        api_key: Optional API key (defaults to ANTHROPIC_API_KEY env var)
        base_url: Optional base URL (defaults to ANTHROPIC_BASE_URL env var)

    Returns:
        Anthropic client or None if not available/configured
    """
    if not ANTHROPIC_AVAILABLE or anthropic is None:
        return None

    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return None

    # Get base URL from parameter or environment
    url = base_url or os.getenv("ANTHROPIC_BASE_URL")

    # Build client kwargs
    client_kwargs: dict[str, Any] = {"api_key": key}
    if url:
        client_kwargs["base_url"] = url

    return anthropic.Anthropic(**client_kwargs)


def extract_actions_from_response(response: str) -> Tuple[str, List[dict]]:
    """
    Extract actions JSON from response and return clean message + actions.
    Returns: (clean_message, actions_list)
    """
    actions: List[dict] = []
    clean_message = response

    # Try to find and parse JSON block
    json_patterns = [
        r'```json\s*(\{[\s\S]*?\})\s*```',
        r'```\s*(\{[\s\S]*?\})\s*```',
    ]

    for pattern in json_patterns:
        match = re.search(pattern, response)
        if match:
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                if "actions" in data:
                    actions = data["actions"]
                    # Remove the JSON block from the message
                    clean_message = re.sub(pattern, '', response).strip()
                    break
            except json.JSONDecodeError:
                continue

    return clean_message, actions


def process_ai_chat_message(
    message: str,
    history: List[dict],
    anthropic_api_key: Optional[str] = None,
    anthropic_base_url: Optional[str] = None,
) -> Generator[Tuple[List[dict], str], None, None]:
    """
    Process a chat message and generate AI response with actions.

    This is a generator that yields (updated_history, actions_json) tuples
    for streaming updates.

    Args:
        message: User's chat message
        history: Chat history in messages format [{"role": "user/assistant", "content": "..."}]
        anthropic_api_key: Optional API key for Anthropic
        anthropic_base_url: Optional base URL for Anthropic API

    Yields:
        Tuple of (updated_history, actions_json_string)
    """
    if not message.strip():
        yield history, ""
        return

    # Add user message to history
    history = history + [{"role": "user", "content": message}]

    # Check if Anthropic is available
    if not ANTHROPIC_AVAILABLE:
        error_msg = "Anthropic SDK 未安装。请运行: pip install anthropic"
        history = history + [{"role": "assistant", "content": error_msg}]
        yield history, ""
        return

    # Get API client
    client = get_anthropic_client(anthropic_api_key, anthropic_base_url)
    if not client:
        error_msg = "请设置 ANTHROPIC_API_KEY 环境变量或在 .env 文件中配置"
        history = history + [{"role": "assistant", "content": error_msg}]
        yield history, ""
        return

    try:
        # Prepare messages for Claude
        system_prompt = get_system_prompt_for_ui()

        # Convert history to Claude format
        messages = []
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Call Claude API with streaming
        full_response = ""
        history_with_assistant = history + [{"role": "assistant", "content": ""}]

        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                # Update the assistant message in history
                history_with_assistant[-1]["content"] = full_response
                yield history_with_assistant, ""

        # Extract actions from complete response
        clean_message, actions = extract_actions_from_response(full_response)

        # Update history with clean message (without JSON block)
        if clean_message != full_response:
            history_with_assistant[-1]["content"] = clean_message

        # Convert actions to JSON string for JavaScript
        actions_json = json.dumps(actions) if actions else ""

        yield history_with_assistant, actions_json

    except Exception as e:
        # Handle all API errors
        error_type = type(e).__name__
        if "APIConnectionError" in error_type:
            error_msg = "无法连接到 Anthropic API。请检查网络连接或代理设置。"
        elif "RateLimitError" in error_type:
            error_msg = "API 请求频率过高，请稍后再试。"
        elif "APIStatusError" in error_type:
            error_msg = f"API 错误: {str(e)}"
        else:
            error_msg = f"发生错误: {str(e)}"

        history = history + [{"role": "assistant", "content": error_msg}]
        yield history, ""


def process_ai_chat_sync(
    message: str,
    history: List[dict],
    anthropic_api_key: Optional[str] = None,
    anthropic_base_url: Optional[str] = None,
) -> Tuple[List[dict], str]:
    """
    Synchronous version of process_ai_chat_message.
    Returns the final result without streaming.
    """
    result = None
    for result in process_ai_chat_message(
        message, history, anthropic_api_key, anthropic_base_url
    ):
        pass
    return result if result else (history, "")


def clear_chat_history() -> Tuple[List[dict], str]:
    """Clear chat history and return empty state"""
    return [], ""


def get_example_prompts() -> List[str]:
    """Get example prompts for the chat interface"""
    return [
        "帮我用 Kling 生成一个日落视频",
        "用 Midjourney 生成一张赛博朋克风格的城市图片",
        "帮我设置 Sora 生成一段海浪拍打沙滩的视频",
        "切换到 Veo3 模型，生成一个森林中的精灵",
        "帮我用 Wan2.5 从图片生成视频",
    ]
