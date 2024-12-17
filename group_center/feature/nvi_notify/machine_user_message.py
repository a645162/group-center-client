from group_center.feature.nvi_notify import notify_api
from group_center.utils.linux.linux_user import get_current_user_name

__all__ = ["machine_user_message_via_local_nvi_notify"]


def machine_user_message_via_local_nvi_notify(
    content: str,
    user_name: str = "",
) -> bool:
    user_name = user_name.strip()

    # If user name is empty, use current user name.
    if user_name == "":
        user_name = get_current_user_name()

    if user_name == "":
        return False

    data_dict: dict = {
        "userName": user_name,
        "content": content,
    }

    try:
        notify_api.send_to_nvi_notify(
            dict_data=data_dict, target="/machine_user_message"
        )

        return True
    except Exception:
        # Ignore all errors to avoid program crash.
        return False
