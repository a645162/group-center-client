import json  # JSON处理 / JSON processing
from typing import Any, Dict, Optional

import requests  # HTTP请求 / HTTP requests
from requests.models import Response  # HTTP响应类型 / HTTP response type

from group_center.core import group_center_encrypt  # 加密模块 / Encryption module
from group_center.core.config_core import (
    MachineConfig,
    get_env_machine_config,
)  # 配置管理 / Configuration management
from group_center.utils.log.logger import get_logger  # 日志模块 / Logging module

# 全局配置变量 / Global configuration variables
GROUP_CENTER_URL: str = ""  # Group Center服务URL / Group Center service URL
MACHINE_NAME_FULL: str = ""  # 完整机器名 / Full machine name
MACHINE_NAME_SHORT: str = ""  # 简短机器名 / Short machine name
MACHINE_PASSWORD: str = ""  # 认证密码 / Authentication password

access_key: str = ""  # 访问密钥 / Access key

group_center_public_part: Dict[str, str] = {
    "serverName": MACHINE_NAME_FULL,
    "serverNameEng": MACHINE_NAME_SHORT,
}  # 公共信息部分 / Public information part

LOGGER: Optional[Any] = None  # 日志对象 / Logger object


def init_logger() -> None:
    """初始化日志对象
    Initialize logger object
    """
    global LOGGER
    if LOGGER is None:
        LOGGER = get_logger()


def set_group_center_host_url(host_url: str) -> None:
    """设置Group Center服务URL
    Set Group Center service URL

    Args:
        host_url (str): 服务URL / Service URL
    """
    global GROUP_CENTER_URL
    GROUP_CENTER_URL = host_url


def set_machine_name_full(server_name: str) -> None:
    """设置完整机器名
    Set full machine name

    Args:
        server_name (str): 完整机器名 / Full machine name
    """
    global MACHINE_NAME_FULL
    MACHINE_NAME_FULL = server_name


def set_machine_name_short(server_name_short: str) -> None:
    """设置简短机器名
    Set short machine name

    Args:
        server_name_short (str): 简短机器名 / Short machine name
    """
    global MACHINE_NAME_SHORT
    MACHINE_NAME_SHORT = server_name_short


def set_machine_password(password: str) -> None:
    """设置认证密码
    Set authentication password

    Args:
        password (str): 认证密码 / Authentication password
    """
    global MACHINE_PASSWORD
    MACHINE_PASSWORD = password


def setup_group_center_by_opt(opt: Any) -> None:
    """通过选项配置Group Center
    Configure Group Center by options

    Args:
        opt (Any): 配置选项 / Configuration options
    """
    if hasattr(opt, "host") and opt.host:
        set_group_center_host_url(opt.host)

    if hasattr(opt, "center_name") and opt.center_name:
        set_machine_name_short(opt.center_name)

    if hasattr(opt, "center_password") and opt.center_password:
        set_machine_password(opt.center_password)

    group_center_login()


def __init_from_env(skip_if_exist: bool = True) -> None:
    """从环境变量初始化配置
    Initialize configuration from environment variables

    Args:
        skip_if_exist (bool): 如果配置已存在则跳过 / Skip if configuration already exists
    """
    if skip_if_exist and GROUP_CENTER_URL != "":
        return

    env_machine_config: Optional[MachineConfig] = get_env_machine_config()

    if env_machine_config is None:
        print("Group Center Config Not Found in Env.")
        return

    set_group_center_host_url(env_machine_config.url)
    set_machine_name_full(env_machine_config.name_full)
    set_machine_name_short(env_machine_config.name_short)
    set_machine_password(env_machine_config.password)


def group_center_get_url(target_api: str) -> str:
    """获取完整的API URL
    Get complete API URL

    Args:
        target_api (str): 目标API路径 / Target API path

    Returns:
        str: 完整的URL / Complete URL
    """
    __init_from_env()

    global GROUP_CENTER_URL

    if GROUP_CENTER_URL.endswith("/"):
        if target_api.startswith("/"):
            target_api = target_api[1:]
    else:
        if not target_api.startswith("/"):
            target_api = "/" + target_api

    return GROUP_CENTER_URL + target_api


def get_public_part() -> Dict[str, str]:
    """获取公共信息部分
    Get public information part

    Returns:
        Dict[str, str]: 包含公共信息的字典 / Dictionary containing public information
    """
    global group_center_public_part

    group_center_public_part.update(
        {
            "serverName": MACHINE_NAME_FULL,
            "serverNameEng": MACHINE_NAME_SHORT,
            "accessKey": get_access_key(),
        }
    )

    return group_center_public_part


def __group_center_login(username: str, password: str) -> bool:
    """内部登录方法
    Internal login method

    Args:
        username (str): 用户名 / Username
        password (str): 密码 / Password

    Returns:
        bool: 登录是否成功 / Whether login is successful
    """
    # Init logger if not set
    init_logger()

    username = username.strip()
    password = password.strip()

    LOGGER.info("[Group Center] Login Start")
    url: str = group_center_get_url(target_api="/auth/client/auth")
    try:
        LOGGER.info(f"[Group Center] Auth To: {url}")
        password_display: str = group_center_encrypt.encrypt_password_to_display(
            password
        )
        password_encoded: str = password
        password_encoded: str = group_center_encrypt.get_password_hash(password_encoded)
        LOGGER.info(
            f"[Group Center] Auth userName:{username} password:{password_display}"
        )

        params = {"userName": username, "password": password_encoded}
        # print(f"[Group Center] Auth params: {params}")

        # 发送GET请求 / Send GET request
        response: Response = requests.get(
            url=url,
            params=params,
            timeout=10,
        )

        if response.status_code != 200:
            LOGGER.error(
                f"[Group Center] Auth Failed({response.status_code}): {response.text}"
            )
            return False

        response_dict: Dict[str, Any] = json.loads(response.text)
        if not (
            "isAuthenticated" in response_dict.keys()
            and response_dict["isAuthenticated"]
        ):
            LOGGER.error("[Group Center] Not authorized")
            return False
        global access_key
        access_key = response_dict["accessKey"]
        LOGGER.info(f"[Group Center] Auth Handshake Success: {access_key}")

    except Exception as e:
        LOGGER.error(f"[Group Center] Auth Handshake Failed: {e}")
        return False

    LOGGER.info("[Group Center] Login Finished.")


def group_center_login() -> bool:
    """Group Center登录
    Group Center login

    Returns:
        bool: 登录是否成功 / Whether login is successful
    """
    __init_from_env()

    return __group_center_login(username=MACHINE_NAME_SHORT, password=MACHINE_PASSWORD)


def get_access_key() -> str:
    """获取访问密钥
    Get access key

    Returns:
        str: 访问密钥 / Access key
    """
    global access_key

    if access_key == "":
        group_center_login()

    return access_key
