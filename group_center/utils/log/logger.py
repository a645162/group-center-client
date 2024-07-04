is_loguru_mode = False

try:
    from group_center.utils.log.backend_loguru import get_loguru_backend

    is_loguru_mode = True
except ImportError:
    is_loguru_mode = False

from group_center.utils.log.backend_logging import get_logging_backend
from group_center.utils.log.backend_print import get_print_backend

__is_print_mode = True


def set_is_print_mode(is_print: bool):
    global __is_print_mode
    __is_print_mode = is_print


logger = None


def __init_logger():
    global logger
    if logger is not None:
        return

    if __is_print_mode:
        logger = get_print_backend()
    else:
        if is_loguru_mode:
            logger = get_loguru_backend()
        else:
            logger = get_logging_backend()


def set_logger(exist_logger):
    global logger
    logger = exist_logger


def get_logger():
    __init_logger()

    global logger
    return logger
