import os
import requests

from group_center.core import group_center_machine
from group_center.utils.log.logger import get_logger

logger = get_logger()


def upload_file(file_path: str, target_api: str, params: dict = None) -> bool:
    target_url = \
        group_center_machine.group_center_get_url(target_api=target_api)

    if params is None:
        params = {}

    try:
        access_key = group_center_machine.get_access_key()
        params.update({"accessKey": access_key})

        logger.debug(f"Upload file: {file_path}")
        logger.debug(f"Target URL: {target_url}")

        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)

            files = {'file': (file_name, f)}

            response = requests.post(
                target_url,
                files=files,
                params=params
            )

        logger.debug(f"Response({response.status_code}): {response.text}")
        if response.status_code != 200:
            return False

    except Exception:
        return False

    return True


def download_file(
        save_path: str,
        target_api: str,
        params: dict = None
) -> bool:
    target_url = \
        group_center_machine.group_center_get_url(target_api=target_api)

    if params is None:
        params = {}

    try:
        access_key = group_center_machine.get_access_key()
        params.update({"accessKey": access_key})

        logger.debug(f"Download file: {target_url}")
        logger.debug(f"Save path: {save_path}")

        response = requests.get(
            target_url,
            params=params
        )

        logger.debug(f"Response({response.status_code}): {response.text}")
        if response.status_code != 200:
            return False

        with open(save_path, 'wb') as f:
            f.write(response.content)

    except Exception:
        return False

    return True


if __name__ == '__main__':
    # Upload Test
    upload_result = \
        upload_file(
            file_path=os.path.expanduser("~/.ssh/authorized_keys"),
            target_api="/api/client/file/ssh_key",
            params={
                "userNameEng": "konghaomin"
            }
        )
    print("upload_result:", upload_result)

    download_result = \
        download_file(
            save_path="./authorized_keys",
            target_api="/api/client/file/ssh_key/authorized_keys",
            params={
                "userNameEng": "konghaomin"
            }
        )
    print("download_result:", download_result)
