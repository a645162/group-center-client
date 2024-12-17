from group_center.feature.nvi_notify.machine_user_message import *
from group_center.user_env import *

global_user_name: str = ""

# 全局开关, 是否启用消息推送(默认: 关闭)
global_enable: bool = False


# 全局开关, 是否启用消息推送
def group_center_set_is_valid(enable: bool = True):
    global global_enable
    global_enable = enable


def group_center_set_user_name(new_user_name: str):
    global global_user_name
    global_user_name = new_user_name.strip()


def push_message(
    content: str,
    user_name: str = "",
    only_first_card_process: bool = True,
) -> bool:
    if only_first_card_process and not is_first_card_process():
        return False

    global global_enable, global_user_name

    if not global_enable:
        return False

    if user_name == "":
        user_name = global_user_name.strip()
    return machine_user_message_via_local_nvi_notify(
        content=content,
        user_name=user_name,
    )
