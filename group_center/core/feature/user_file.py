import os
import requests

from group_center.core import group_center_machine


def upload_file(file_path: str, target_api: str, params: dict = None) -> bool:
    target_url = \
        group_center_machine.group_center_get_url(target_api=target_api)

    if params is None:
        params = {}

    try:
        access_key = group_center_machine.get_access_key()
        params.update({"accessKey": access_key})

        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)

            files = {'file': (file_name, f)}

            response = requests.post(
                target_url,
                files=files,
                params=params
            )

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

        response = requests.get(
            target_url,
            params=params
        )

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
