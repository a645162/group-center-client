from typing import List


class LogLevelObject:
    level: int
    level_name: str
    level_threshold: int

    level_color: str = ""
    foreground_color: str = ""
    background_color: str = ""

    def __init__(self):
        self.level = 0
        self.level_name = ""
        self.level_threshold = 0

    def is_valid(self) -> bool:
        return (
                self.level > 0 and
                0 < self.level_threshold <= self.level
        )

    def __int__(self):
        return self.level


class LogLevel:
    __level_list: List[LogLevelObject]

    __current_level: LogLevelObject

    DEBUG: LogLevelObject
    INFO: LogLevelObject
    SUCCESS: LogLevelObject
    WARNING: LogLevelObject
    ERROR: LogLevelObject
    CRITICAL: LogLevelObject

    def __init__(self):
        self.__level_list = []

        self.DEBUG = LogLevelObject()
        self.INFO = LogLevelObject()
        self.SUCCESS = LogLevelObject()
        self.WARNING = LogLevelObject()
        self.ERROR = LogLevelObject()
        self.CRITICAL = LogLevelObject()

        self.__level_list.append(self.DEBUG)
        self.__level_list.append(self.INFO)
        self.__level_list.append(self.SUCCESS)
        self.__level_list.append(self.WARNING)
        self.__level_list.append(self.ERROR)
        self.__level_list.append(self.CRITICAL)

        self.DEBUG.level_name = "DEBUG"
        self.DEBUG.level_color = "blue"
        self.DEBUG.foreground_color = "blue"
        self.DEBUG.background_color = ""

        self.INFO.level_name = "INFO"
        self.INFO.level_color = ""
        self.INFO.foreground_color = ""
        self.INFO.background_color = ""

        self.SUCCESS.level_name = "SUCCESS"
        self.SUCCESS.level_color = "green"
        self.SUCCESS.foreground_color = "green"
        self.SUCCESS.background_color = ""

        self.WARNING.level_name = "WARNING"
        self.WARNING.level_color = "yellow"
        self.WARNING.foreground_color = "yellow"
        self.WARNING.background_color = ""

        self.ERROR.level_name = "ERROR"
        self.ERROR.level_color = "red"
        self.ERROR.foreground_color = "red"
        self.ERROR.background_color = ""

        self.CRITICAL.level_name = "CRITICAL"
        self.CRITICAL.level_color = "cyan"
        self.CRITICAL.foreground_color = "cyan"
        self.CRITICAL.background_color = "on_red"

        for index, level in enumerate(self.__level_list):
            level.level = index + 1

        self.current_level = self.INFO

    @property
    def current_level(self) -> LogLevelObject:
        return self.__current_level

    @current_level.setter
    def current_level(self, value: int):
        if isinstance(value, LogLevelObject):
            self.__current_level = value
            self.update_level_threshold()
            return

        if not isinstance(value, int):
            value = int(value)

        for level in self.__level_list:
            if level.level == value:
                self.__current_level = level
                self.update_level_threshold()
                return

        raise ValueError("Invalid log level")

    def update_level_threshold(self):
        for level in self.__level_list:
            level.level_threshold = self.current_level.level

    def get_loguru_level(self):
        return self.__current_level.level_name

    def get_logging_level(self):
        import logging

        level_name = self.__current_level.level_name

        # Replace SUCCESS with INFO
        if level_name == "SUCCESS":
            level_name = "INFO"

        return getattr(logging, level_name)


__log_level = LogLevel()


def get_log_level() -> LogLevel:
    return __log_level
