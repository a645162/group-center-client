from group_center.core.feature.machine_message import new_message_enqueue


def machine_user_message_directly(
        user_name: str,
        content: str,
):
    data_dict: dict = {
        "userName": user_name,
        "content": content,
    }

    new_message_enqueue(data_dict, "/api/client/user/message")
