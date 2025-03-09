from datetime import datetime
from group_center.feature.nvi_notify.machine_user_message import (
    machine_user_message_via_local_nvi_notify,
)
from group_center.user_env import is_first_card_process

# 全局用户名 (Global user name)
global_user_name: str = ""

# 消息推送开关 (Message push enable flag)
global_enable: bool = False


def group_center_set_is_valid(enable: bool = True) -> None:
    """启用/禁用消息推送 (Enable/Disable message push)

    Args:
        enable (bool, optional): 是否启用 (Enable flag). Defaults to True.
    """
    global global_enable
    global_enable = enable


def group_center_set_user_name(new_user_name: str) -> None:
    """设置全局用户名 (Set global user name)

    Args:
        new_user_name (str): 新用户名 (New user name)
    """
    global global_user_name
    global_user_name = new_user_name.strip()


def push_message(
    content: str, user_name: str = "", only_first_card_process: bool = True
) -> bool:
    """推送消息到通知系统 (Push message to notification system)

    Args:
        content (str): 消息内容 (Message content)
        user_name (str, optional): 目标用户名 (Target user name). Defaults to "".
        only_first_card_process (bool, optional): 仅主卡进程发送 (Only first GPU process sends). Defaults to True.

    Returns:
        bool: 推送是否成功 (Push success flag)
    """
    if only_first_card_process and not is_first_card_process():
        return False

    global global_enable, global_user_name

    if not global_enable:
        return False

    if not user_name:
        user_name = global_user_name.strip()

    return machine_user_message_via_local_nvi_notify(
        content=content, user_name=user_name
    )


if __name__ == "__main__":
    group_center_set_is_valid(True)
    group_center_set_user_name("konghaomin")

    import datetime

    now: datetime = datetime.datetime.now()
    now_str: str = now.strftime("%Y-%m-%d %H:%M:%S")

    push_message(f"测试消息推送: {now_str}")
    print("消息推送完毕！")
