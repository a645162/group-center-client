from group_center.core.feature.machine_message import new_message_enqueue


def machine_message_directly(
    server_name: str, server_name_eng: str, content: str, at: str = "", enable_retry: bool = True
):
    """直接发送机器消息
    Send machine message directly

    Args:
        server_name (str): 服务器名称 / Server name
        server_name_eng (str): 服务器英文名称 / Server English name
        content (str): 消息内容 / Message content
        at (str, optional): @的用户 / User to @. Defaults to "".
        enable_retry (bool, optional): 是否启用重发机制 / Whether to enable retry mechanism. Defaults to True.
    """
    data_dict: dict = {
        "serverName": server_name,
        "serverNameEng": server_name_eng,
        "content": content,
        "at": at,
    }

    new_message_enqueue(data_dict, "/api/client/machine/message", enable_retry=enable_retry)


def machine_user_message_directly(
    user_name: str,
    content: str,
    enable_retry: bool = True
):
    """直接发送用户消息
    Send user message directly

    Args:
        user_name (str): 用户名 / User name
        content (str): 消息内容 / Message content
        enable_retry (bool, optional): 是否启用重发机制 / Whether to enable retry mechanism. Defaults to True.
    """
    data_dict: dict = {
        "userName": user_name,
        "content": content,
    }

    new_message_enqueue(data_dict, "/api/client/user/message", enable_retry=enable_retry)


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
