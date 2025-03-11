from termcolor import colored

from group_center.utils.log.log_level import get_log_level, LogLevel

log_level = get_log_level()
log_level.current_level = log_level.DEBUG


def print_with_level(message: str, current_level: LogLevel) -> None:
    """根据日志级别打印带颜色的日志信息
    Print colored log message according to log level

    Args:
        message: 日志信息 / Log message
        current_level: 日志级别 / Log level
    """
    tag = f"[{current_level.level_name}]"

    final_text = tag + message

    foreground_color = current_level.foreground_color.lower().strip()
    background_color = current_level.background_color.lower().strip()

    if not (foreground_color or background_color or current_level.level_color):
        print(final_text)
        return

    if not (foreground_color and background_color):
        foreground_color = current_level.level_color
        background_color = ""

    if background_color:
        print(
            colored(text=final_text, color=foreground_color, on_color=background_color)
        )
    else:
        print(colored(text=final_text, color=foreground_color))


class BackendPrint:
    """打印样式日志后端
    Print styled logging backend"""

    class Level:
        """日志级别枚举
        Log level enum"""

        INFO = 0
        ERROR = 1
        WARNING = 2
        DEBUG = 3

    level: Level = 0

    def __init__(self):
        """初始化打印样式日志后端
        Initialize print styled logging backend"""
        self.level = self.Level.INFO

    def set_level(self, level: Level) -> None:
        """设置日志级别
        Set log level

        Args:
            level: 日志级别 / Log level
        """
        self.level = level

    def debug(self, message: str) -> None:
        """打印调试级别日志
        Print debug level log

        Args:
            message: 日志信息 / Log message
        """
        print_with_level(message=message, current_level=get_log_level().DEBUG)

    def info(self, message: str) -> None:
        """打印信息级别日志
        Print info level log

        Args:
            message: 日志信息 / Log message
        """
        print_with_level(message=message, current_level=get_log_level().INFO)

    def success(self, message: str) -> None:
        """打印成功级别日志
        Print success level log

        Args:
            message: 日志信息 / Log message
        """
        print_with_level(message=message, current_level=get_log_level().SUCCESS)

    def error(self, message: str) -> None:
        """打印错误级别日志
        Print error level log

        Args:
            message: 日志信息 / Log message
        """
        print_with_level(message=message, current_level=get_log_level().ERROR)

    def warning(self, message: str) -> None:
        """打印警告级别日志
        Print warning level log

        Args:
            message: 日志信息 / Log message
        """
        print_with_level(message=message, current_level=get_log_level().WARNING)

    def critical(self, message: str) -> None:
        """打印严重级别日志
        Print critical level log

        Args:
            message: 日志信息 / Log message
        """
        print_with_level(message=message, current_level=get_log_level().CRITICAL)


print_backend = None


def get_print_backend() -> BackendPrint:
    """获取打印样式日志后端实例
    Get print styled logging backend instance

    Returns:
        BackendPrint: 打印样式日志后端实例 / Print styled logging backend instance
    """
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

    print()
