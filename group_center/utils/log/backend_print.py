from termcolor import colored

from group_center.utils.log.log_level import get_log_level, LogLevelObject

log_level = get_log_level()
log_level.current_level = log_level.DEBUG


def print_with_level(message: str, current_level: LogLevelObject):
    if not current_level.is_valid():
        return

    tag = f"[{current_level.level_name}]"

    final_text = tag + message

    foreground_color = current_level.foreground_color.lower().strip()
    background_color = current_level.background_color.lower().strip()

    if not (
            foreground_color or
            background_color or
            current_level.level_color
    ):
        print(final_text)
        return

    if not (foreground_color and background_color):
        foreground_color = current_level.level_color
        background_color = ""

    if background_color:
        print(
            colored(
                text=final_text,
                color=foreground_color,
                on_color=background_color
            )
        )
    else:
        print(
            colored(
                text=final_text,
                color=foreground_color
            )
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


if __name__ == "__main__":
    print_backend = get_print_backend()

    print_backend.debug("Debug message")
    print_backend.info("Info message")
    print_backend.success("Success message")
    print_backend.warning("Warning message")
    print_backend.error("Error message")
    print_backend.critical("Critical message")
