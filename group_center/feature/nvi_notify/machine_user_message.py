from group_center.feature.nvi_notify import notify_api
from group_center.utils.linux.linux_user import get_current_user_name

__all__ = [
    "machine_user_message_via_local_nvi_notify"
]  # 导出列表 / Export list


def machine_user_message_via_local_nvi_notify(
    content: str,  # 消息内容 / Message content
    user_name: str = "",  # 用户名，默认为空 / Username, default empty
) -> bool:
    """
    通过本地NVI通知发送机器用户消息
    Send machine user message via local NVI notify

    Args:
        content (str): 要发送的消息内容 / Message content to send
        user_name (str): 目标用户名 / Target username

    Returns:
        bool: 是否发送成功 / Whether the message was sent successfully
    """
    user_name = user_name.strip()

    # If user name is empty, use current user name.
    # 如果用户名为空，使用当前用户名
    if user_name == "":
        user_name: str = (
            get_current_user_name()
        )  # 获取当前用户名 / Get current username

    if user_name == "":
        return False

    data_dict: dict[str, str] = {  # 请求数据字典 / Request data dictionary
        "userName": user_name,
        "content": content,
    }

    try:
        notify_api.send_to_nvi_notify(  # 发送NVI通知 / Send NVI notify
            dict_data=data_dict,
            target="/machine_user_message",  # 目标路径 / Target path
        )

        return True
    except Exception:  # 捕获所有异常 / Catch all exceptions
        # Ignore all errors to avoid program crash.
        # 忽略所有错误以避免程序崩溃
        return False
