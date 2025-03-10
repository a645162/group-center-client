import os
from typing import Tuple


def ENV_SCREEN_NAME_FULL() -> str:
    """获取Screen会话全名 (Get full Screen session name)

    Returns:
        str: Screen会话全名 (Full Screen session name)
    """
    return os.getenv("STY", "").strip()


def _parse_screen_name() -> Tuple[str, str]:
    """解析Screen会话名称 (Parse Screen session name)

    Returns:
        Tuple[str, str]: (会话ID, 会话名称) (Session ID, Session name)
    """
    full_name = ENV_SCREEN_NAME_FULL()
    parts = full_name.split(".") if full_name else []
    if len(parts) < 2:
        return ("", "")
    return (parts[0], ".".join(parts[1:]).strip())


def ENV_SCREEN_SESSION_ID() -> str:
    """获取Screen会话ID (Get Screen session ID)

    Returns:
        str: 屏幕会话ID (Screen session ID)
    """
    return _parse_screen_name()[0]


def ENV_SCREEN_SESSION_NAME() -> str:
    """获取Screen会话名称 (Get Screen session name)

    Returns:
        str: 屏幕会话名称 (Screen session name)
    """
    return _parse_screen_name()[1]


def is_in_screen_session() -> bool:
    """检查是否在Screen会话中 (Check if in Screen session)

    Returns:
        bool: 是否在Screen会话中 (是否在Screen会话中)
    """
    return ENV_SCREEN_SESSION_NAME() != ""
