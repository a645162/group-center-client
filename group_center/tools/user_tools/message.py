import os

from group_center.feature.nvi_notify.machine_user_message import (
    machine_user_message_via_local_nvi_notify,
)
from group_center.tools.user_env import is_first_card_process
from .config import global_enable_status, global_user_name_status

from group_center.utils.log.logger import get_logger

LOGGER = get_logger("user_message")


def push_message(
    content: str, user_name: str = "", only_first_card_process: bool = True
) -> bool:
    """推送消息到通知系统 (Push message to notification system)
    Push message to notification system

    Args:
        content (str): 消息内容 (Message content)
        user_name (str, optional): 目标用户名 (Target user name). Defaults to "".
        only_first_card_process (bool, optional): 仅主卡进程发送 (Only first GPU process sends). Defaults to True.

    Returns:
        bool: 推送是否成功 (Push success flag)
    """
    if only_first_card_process and not is_first_card_process():
        LOGGER.debug("[Group Center] 非主卡进程，不发送消息！")
        return False

    if not global_enable_status():
        LOGGER.debug("[Group Center] 消息推送被禁用！")
        return False

    if not user_name:
        user_name = global_user_name_status().strip()

    LOGGER.debug(f"[Group Center] 发送消息到用户 ({user_name}): {content}")

    # Check Env "NVI_NOTIFY_IGNORE_USER_MSG"
    if os.getenv("NVI_NOTIFY_IGNORE_USER_MSG", "0") == "1":
        LOGGER.debug("[Group Center] 环境变量 NVI_NOTIFY_IGNORE_USER_MSG=1，忽略发送消息")
        return False

    return machine_user_message_via_local_nvi_notify(
        content=content, user_name=user_name
    )


if __name__ == "__main__":
    pass
