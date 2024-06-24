from group_center.feature.nvi_notify import notify_api


def machine_user_message(
        user_name: str,
        content: str,
):
    data_dict: dict = {
        "userName": user_name,
        "content": content,
    }

    notify_api.send_to_nvi_notify(
        dict_data=data_dict,
        target="/machine_user_message"
    )
