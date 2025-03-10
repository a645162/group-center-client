import requests
from typing import Dict, Any

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
    response = requests.post(
        get_nvi_notify_api_url(target), data=dict_data
    )  # 发送POST请求 / Send POST request

    return response.status_code == 200  # 返回是否成功 / Return whether successful
