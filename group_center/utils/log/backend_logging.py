import logging

from group_center.utils.log.log_level import get_log_level


def get_logging():
    log_level = get_log_level()

    logging.basicConfig(
        level=log_level.get_logging_level(),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)


def get_logging_backend():
    return get_logging()
