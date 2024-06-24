from group_center.feature.nvi_notify import notify_api


def machine_user_message_via_local_nvi_notify(
        user_name: str,
        content: str,
):
    data_dict: dict = {
        "userName": user_name,
        "content": content,
    }

    try:
        notify_api.send_to_nvi_notify(
            dict_data=data_dict,
            target="/machine_user_message"
        )
    except Exception:
        # Ignore all errors to avoid program crash.
        pass
