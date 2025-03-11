import os
import requests

from group_center.core import group_center_machine
from group_center.utils.log.logger import get_logger

LOGGER = get_logger()


def upload_file(file_path: str, target_api: str, params: dict = None) -> bool:
    """上传用户文件到群组中心
    Upload user file to group center

    Args:
        file_path (str): 文件路径 / File path
        target_api (str): 目标API路径 / Target API path
        params (dict, optional): 请求参数 / Request parameters. Defaults to None.

    Returns:
        bool: 上传是否成功 / Whether upload is successful
    """
    target_url = group_center_machine.group_center_get_url(target_api=target_api)

    if params is None:
        params = {}

    try:
        access_key = group_center_machine.get_access_key()
        params.update({"accessKey": access_key})

        LOGGER.debug(f"Upload file: {file_path}")
        LOGGER.debug(f"Target URL: {target_url}")

        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)

            files = {"file": (file_name, f)}

            response = requests.post(target_url, files=files, params=params)

        LOGGER.debug(f"Response({response.status_code}): {response.text}")
        if response.status_code != 200:
            return False

    except Exception:
        return False

    return True


def download_file(save_path: str, target_api: str, params: dict = None) -> bool:
    """从群组中心下载用户文件
    Download user file from group center

    Args:
        save_path (str): 文件保存路径 / File save path
        target_api (str): 目标API路径 / Target API path
        params (dict, optional): 请求参数 / Request parameters. Defaults to None.

    Returns:
        bool: 下载是否成功 / Whether download is successful
    """
    target_url = group_center_machine.group_center_get_url(target_api=target_api)

    if params is None:
        params = {}

    try:
        access_key = group_center_machine.get_access_key()
        params.update({"accessKey": access_key})

        LOGGER.debug(f"Download file: {target_url}")
        LOGGER.debug(f"Save path: {save_path}")

        response = requests.get(target_url, params=params)

        LOGGER.debug(f"Response({response.status_code}): {response.text}")
        if response.status_code != 200:
            return False

        with open(save_path, "wb") as f:
            f.write(response.content)

    except Exception:
        return False

    return True


if __name__ == "__main__":
    # Upload Test
    upload_result = upload_file(
        file_path=os.path.expanduser("~/.ssh/authorized_keys"),
        target_api="/api/client/file/ssh_key",
        params={"userNameEng": "konghaomin"},
    )
    print("upload_result:", upload_result)

    download_result = download_file(
        save_path="./authorized_keys",
        target_api="/api/client/file/ssh_key/authorized_keys",
        params={"userNameEng": "konghaomin"},
    )
    print("download_result:", download_result)
