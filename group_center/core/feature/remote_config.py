import time

import requests

from group_center.core import group_center_machine
from group_center.utils.log.logger import get_logger

logger = get_logger()

max_retry_times = 5


def get_json_str(target_api: str) -> str:
    url = group_center_machine.group_center_get_url(target_api=target_api)

    for _ in range(max_retry_times):
        try:
            access_key = group_center_machine.get_access_key()

            params = {"accessKey": access_key}
            response = requests.get(url=url, params=params, timeout=10)

            text = response.text.strip()

            if response.status_code == 200:
                return text

            logger.error("[Group Center]" + text)
        except Exception as e:
            logger.error("get user config json error" + str(e))

        time.sleep(10)

    return ""


def get_user_config_json_str() -> str:
    return get_json_str(target_api="/api/client/config/user_list")


def get_machine_config_json_str() -> str:
    return get_json_str(target_api="/api/client/config/machine_list")


def get_env_json_str() -> str:
    return get_json_str(target_api="/api/client/config/env_list")


if __name__ == "__main__":
    json_text = get_user_config_json_str()
    print(json_text)

    print()
