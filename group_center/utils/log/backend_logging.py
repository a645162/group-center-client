from group_center.utils.log.log_level import get_log_level
from group_center.utils.log import new_logging


def __setup_logging():
    log_level = get_log_level()

    new_logging.basicConfig(
        level=log_level.get_logging_level(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def get_logging_backend():
    __setup_logging()

    return new_logging
