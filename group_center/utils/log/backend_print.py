import colorama

from group_center.utils.log import print_color
from group_center.utils.log.log_level import get_log_level, LogLevelObject


def print_with_level(message: str, current_level: LogLevelObject):
    if not current_level.is_valid():
        return

    tag = f"[{current_level.level_name}]"

    foreground_color = current_level.foreground_color.upper().strip()
    background_color = current_level.background_color.upper().strip()

    if not (foreground_color and background_color):
        foreground_color = current_level.level_color
        background_color = ""

    print_color.print_color(
        message=tag + message,
        color=foreground_color,
        background_color=background_color,
        end="\n"
    )


class BackendPrint:
    class Level:
        INFO = 0
        ERROR = 1
        WARNING = 2
        DEBUG = 3

    level: Level = 0

    def __init__(self):
        self.level = self.Level.INFO

    def set_level(self, level: Level):
        self.level = level

    def debug(self, message):
        print_with_level(
            message=message,
            current_level=get_log_level().DEBUG
        )

    def info(self, message):
        print_with_level(
            message=message,
            current_level=get_log_level().INFO
        )

    def success(self, message):
        print_with_level(
            message=message,
            current_level=get_log_level().SUCCESS
        )

    def error(self, message):
        print_with_level(
            message=message,
            current_level=get_log_level().ERROR
        )

    def warning(self, message):
        print_with_level(
            message=message,
            current_level=get_log_level().WARNING
        )

    def critical(self, message):
        print_with_level(
            message=message,
            current_level=get_log_level().CRITICAL
        )


print_backend = None


def get_print_backend():
    global print_backend

    if print_backend is None:
        print_backend = BackendPrint()

    return print_backend
