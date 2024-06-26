from group_center.feature.nvi_notify.machine_user_message import *

global_user_name: str = ""


def set_group_center_user_name(new_user_name: str):
    global global_user_name
    global_user_name = new_user_name.strip()


def push_message(content: str, user_name: str = ""):
    global global_user_name
    if user_name == "":
        user_name = global_user_name.strip()
    return machine_user_message_via_local_nvi_notify(
        content=content,
        user_name=user_name,
    )
