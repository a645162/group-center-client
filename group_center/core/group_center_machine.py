import json

import loguru
import requests

from group_center.core import group_center_encrypt
from group_center.utils.logger import get_logger

GROUP_CENTER_URL = ""
MACHINE_NAME_FULL = ""
MACHINE_NAME_SHORT = ""
MACHINE_PASSWORD = ""

access_key = ""

group_center_public_part: dict = {
    "serverName": MACHINE_NAME_FULL,
    "serverNameEng": MACHINE_NAME_SHORT,
}

logger: loguru.logger


def init_logger():
    global logger
    if logger is None:
        logger = get_logger()


def set_logger(exist_logger: loguru.logger):
    global logger
    logger = exist_logger


def set_group_center_host(host_url: str):
    global GROUP_CENTER_URL
    GROUP_CENTER_URL = host_url


def set_server_name(server_name: str):
    global MACHINE_NAME_FULL
    MACHINE_NAME_FULL = server_name


def set_server_name_short(server_name_short: str):
    global MACHINE_NAME_SHORT
    MACHINE_NAME_SHORT = server_name_short


def group_center_get_url(target_api: str):
    if GROUP_CENTER_URL.endswith("/"):
        if target_api.startswith("/"):
            target_api = target_api[1:]
    else:
        if not target_api.startswith("/"):
            target_api = "/" + target_api

    return GROUP_CENTER_URL + target_api


def get_public_part() -> dict:
    global group_center_public_part

    group_center_public_part.update({
        "serverName": MACHINE_NAME_FULL,
        "serverNameEng": MACHINE_NAME_SHORT,
        "accessKey": get_access_key(),
    })

    return group_center_public_part


def __group_center_login(username: str, password: str) -> bool:
    # Init logger if not set
    init_logger()

    logger.info("[Group Center] Login Start")
    url = group_center_get_url(target_api="/auth/client/auth")
    try:
        logger.info(f"[Group Center] Auth To: {url}")
        password_display = \
            group_center_encrypt.encrypt_password_to_display(password)
        password_encoded = \
            group_center_encrypt.get_password_hash(password)
        logger.info(
            f"[Group Center] Auth userName:{username} password:{password_display}"
        )

        response = requests.get(
            url=url,
            params={"userName": username, "password": password_encoded},
            timeout=10,
        )

        if response.status_code != 200:
            logger.error(f"[Group Center] Auth Failed: {response.text}")
            return False

        response_dict: dict = json.loads(response.text)
        if not (
                "isAuthenticated" in response_dict.keys()
                and response_dict["isAuthenticated"]
        ):
            logger.error("[Group Center] Not authorized")
            return False
        global access_key
        access_key = response_dict["accessKey"]
        logger.info(f"[Group Center] Auth Handshake Success: {access_key}")

    except Exception as e:
        logger.error(f"[Group Center] Auth Handshake Failed: {e}")
        return False

    logger.info("[Group Center] Login Finished.")


def group_center_login() -> bool:
    return __group_center_login(
        username=MACHINE_NAME_SHORT, password=MACHINE_PASSWORD
    )


def get_access_key() -> str:
    global access_key

    if access_key == "":
        group_center_login()

    return access_key
