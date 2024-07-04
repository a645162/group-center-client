from group_center.utils.log.log_level import get_log_level


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
        get_log_level().DEBUG.is_valid()
        print(message)

    def info(self, message):
        get_log_level().INFO.is_valid()
        print(message)

    def success(self, message):
        get_log_level().INFO.is_valid()
        print(message)

    def error(self, message):
        get_log_level().ERROR.is_valid()
        print(message)

    def warning(self, message):
        get_log_level().WARNING.is_valid()
        print(message)

    def critical(self, message):
        get_log_level().CRITICAL.is_valid()
        print(message)


print_backend = None


def get_print_backend():
    global print_backend

    if print_backend is None:
        print_backend = BackendPrint()

    return print_backend
