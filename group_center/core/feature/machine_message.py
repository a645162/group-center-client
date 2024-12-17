import json
import queue
import threading
import time
from queue import Queue
from typing import List

import requests

from group_center.core import group_center_machine
from group_center.utils.log.logger import get_logger


logger = get_logger()


def send_dict_to_center(data: dict, target: str) -> bool:
    data_dict = {}
    data_dict.update(data)

    # For Java Spring Boot JSON Deserializer
    # https://blog.csdn.net/lijingjingchn/article/details/120553128

    # Find out all bool keys
    bool_keys_list: List[str] = []
    for key in data_dict.keys():
        if isinstance(data_dict[key], bool):
            bool_keys_list.append(key)

    # Clone all bool keys to new keys
    for key in bool_keys_list:
        if key.startswith("is"):
            new_key = key[2:]

            # Check first letter is upper or not
            if new_key[0].isupper():
                new_key = new_key[0].lower() + new_key[1:]

            data_dict[new_key] = data_dict[key]

    url = group_center_machine.group_center_get_url(target_api=target)
    try:
        response = requests.post(
            url=url,
            params=group_center_machine.get_public_part(),
            json=data_dict,
            timeout=10,
        )

        response_dict: dict = json.loads(response.text)

        if not (
            "isAuthenticated" in response_dict.keys()
            and response_dict["isAuthenticated"]
        ):
            logger.error("[Group Center] Not authorized")
            group_center_machine.group_center_login()
            return False

        if not ("isSucceed" in response_dict.keys() and response_dict["isSucceed"]):
            logger.error(f"[Group Center] Send {target} Failed: {response.text}")
            return False

        logger.info(f"[Group Center] Send {target} Success")
        return True
    except Exception as e:
        logger.error(f"[Group Center] Send {target} Failed: {e}")
        return False


task_queue: Queue = Queue()


class GroupCenterWorkThread(threading.Thread):
    def __init__(self):
        super(GroupCenterWorkThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            group_center_machine.get_access_key()

            try:
                data, target = task_queue.get(timeout=10)
                if send_dict_to_center(data=data, target=target):
                    task_queue.task_done()
                else:
                    # 发送失败，将任务放回队列，以便重试
                    task_queue.put((data, target))
                    # 多休息一会儿再重试
                    time.sleep(20)
            except queue.Empty:
                pass
            except Exception as e:
                logger.error(f"[GroupCenter] Thread exception: {e}")


work_thread = None


def new_message_enqueue(data: dict, target: str):
    global task_queue, work_thread

    task_queue.put((data, target))

    if work_thread is not None and not work_thread.is_alive():
        work_thread = None

    if work_thread is None:
        work_thread = GroupCenterWorkThread()
        work_thread.start()
