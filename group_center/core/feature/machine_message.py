import json
import queue
import threading
import time
from queue import Queue
from typing import List

import requests

from group_center.core import group_center_machine
from group_center.utils.log.logger import get_logger


LOGGER = get_logger()


def send_dict_to_center(data: dict, target: str) -> bool:
    """发送字典数据到中心
    Send dictionary data to center

    Args:
        data (dict): 要发送的数据 / Data to send
        target (str): 目标API路径 / Target API path

    Returns:
        bool: 是否发送成功 / Whether the send was successful
    """
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
            LOGGER.error("[Group Center] Not authorized")
            group_center_machine.group_center_login()
            return False

        if not ("isSucceed" in response_dict.keys() and response_dict["isSucceed"]):
            LOGGER.error(f"[Group Center] Send {target} Failed: {response.text}")
            return False

        LOGGER.info(f"[Group Center] Send {target} Success")
        return True
    except Exception as e:
        LOGGER.error(f"[Group Center] Send {target} Failed: {e}")
        return False


# 重发队列 - 用于重要消息，失败会重试
retry_queue: Queue = Queue()

# 无重发队列 - 用于心跳包等不重要消息，失败不重试
no_retry_queue: Queue = Queue()


class GroupCenterWorkThread(threading.Thread):
    """Group Center 工作线程
    Group Center work thread
    """

    def __init__(self):
        super(GroupCenterWorkThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        """停止线程
        Stop the thread
        """
        self._stop_event.set()

    def run(self):
        """线程主循环
        Thread main loop
        """
        while not self._stop_event.is_set():
            group_center_machine.get_access_key()

            # 优先处理无重发队列（心跳包等）
            try:
                data, target = no_retry_queue.get(timeout=1)
                send_dict_to_center(data=data, target=target)
                no_retry_queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                LOGGER.error(f"[GroupCenter] No-retry queue exception: {e}")
                no_retry_queue.task_done()  # 无重发队列即使失败也标记完成

            # 处理重发队列（重要消息）
            try:
                data, target = retry_queue.get(timeout=10)
                if send_dict_to_center(data=data, target=target):
                    retry_queue.task_done()
                else:
                    # 发送失败，将任务放回队列，以便重试
                    # Send failed, put task back to queue for retry
                    retry_queue.put((data, target))
                    # 多休息一会儿再重试
                    # Sleep longer before retry
                    time.sleep(20)
            except queue.Empty:
                pass
            except Exception as e:
                LOGGER.error(f"[GroupCenter] Retry queue exception: {e}")


work_thread = None


def new_message_enqueue(data: dict, target: str, enable_retry: bool = True):
    """将新消息加入队列
    Enqueue new message

    Args:
        data (dict): 消息数据 / Message data
        target (str): 目标API路径 / Target API path
        enable_retry (bool): 是否启用重发机制 / Whether to enable retry mechanism
    """
    global retry_queue, no_retry_queue, work_thread

    if enable_retry:
        retry_queue.put((data, target))
    else:
        no_retry_queue.put((data, target))

    if work_thread is not None and not work_thread.is_alive():
        work_thread = None

    if work_thread is None:
        work_thread = GroupCenterWorkThread()
        work_thread.start()


def send_message_directly(data: dict, target: str) -> bool:
    """直接发送消息（无队列，无重发）
    Send message directly (no queue, no retry)

    Args:
        data (dict): 消息数据 / Message data
        target (str): 目标API路径 / Target API path

    Returns:
        bool: 是否发送成功 / Whether the send was successful
    """
    return send_dict_to_center(data=data, target=target)
