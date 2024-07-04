from typing import List


class LogLevelObject:
    level: int
    level_name: str
    level_threshold: int

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
        self.INFO.level_name = "INFO"
        self.SUCCESS.level_name = "SUCCESS"
        self.WARNING.level_name = "WARNING"
        self.ERROR.level_name = "ERROR"
        self.CRITICAL.level_name = "CRITICAL"

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
