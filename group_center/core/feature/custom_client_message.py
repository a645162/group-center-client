from group_center.core.feature.machine_message import new_message_enqueue


def machine_message_directly(
    server_name: str, server_name_eng: str, content: str, at: str = ""
):
    data_dict: dict = {
        "serverName": server_name,
        "serverNameEng": server_name_eng,
        "content": content,
        "at": at,
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
    machine_message_directly(
        server_name="3090",
        server_name_eng="3090",
        content="Test group message",
        at="孔昊旻",
    )

    machine_user_message_directly(
        user_name="konghaomin", content="Test personal message"
    )
