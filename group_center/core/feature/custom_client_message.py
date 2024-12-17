from group_center.core.feature.machine_message import new_message_enqueue


def machine_message_directly(
    machine_name: str,
    machine_name_eng: str,
    content: str,
):
    data_dict: dict = {
        "serverName": machine_name,
        "serverNameEng": machine_name_eng,
        "content": content,
    }

    new_message_enqueue(data_dict, "/api/client/machine/message")


def machine_user_message_directly(
    user_name: str,
    content: str,
):
    data_dict: dict = {
        "userName": user_name,
        "content": content,
    }

    new_message_enqueue(data_dict, "/api/client/user/message")


if __name__ == "__main__":
    machine_message_directly("3090", "3090", "Test group message")
    machine_user_message_directly("konghaomin", "Test personal message")
