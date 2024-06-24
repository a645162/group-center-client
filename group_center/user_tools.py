from group_center.feature.nvi_notify.machine_user_message import *


def push_message(content: str, user_name: str = ""):
    return machine_user_message_via_local_nvi_notify(
        content=content,
        user_name=user_name,
    )
