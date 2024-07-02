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

    def info(self, message):
        print(message)

    def error(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def debug(self, message):
        print(message)


print_backend = None


def get_print_backend():
    global print_backend

    if print_backend is None:
        print_backend = BackendPrint()

    return print_backend
