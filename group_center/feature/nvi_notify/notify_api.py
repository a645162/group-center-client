import requests
from typing import Dict, Any

from group_center.utils.log.logger import get_logger

LOGGER = get_logger("user_message")

url: str = "http://localhost:8080"  # NVI通知API的基础URL / Base URL for NVI notify API


def get_nvi_notify_api_url(target: str) -> str:
    """
    获取完整的NVI通知API URL
    Get complete NVI notify API URL

    Args:
        target (str): API路径 / API path

    Returns:
        str: 完整的API URL / Complete API URL
    """
    return url.strip() + target.strip()


def send_to_nvi_notify(dict_data: Dict[str, Any], target: str) -> bool:
    """
    发送数据到NVI通知API
    Send data to NVI notify API

    Args:
        dict_data: 要发送的数据字典 / Data dictionary to send
        target: API路径 / API path

    Returns:
        bool: 是否发送成功 / Whether the request was successful
    """

    LOGGER.debug(
        f"[NVI Notify] 发送数据到 {get_nvi_notify_api_url(target)}: {dict_data}"
    )

    response = requests.post(
        get_nvi_notify_api_url(target),
        data=dict_data,
        proxies={"http": None, "https": None},
    )  # 发送POST请求 / Send POST request，不使用http_proxy

    LOGGER.debug(
        f"[NVI Notify] 响应状态码: {response.status_code}, 响应内容: {response.text}"
    )

    return response.status_code == 200  # 返回是否成功 / Return whether successful
