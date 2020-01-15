from .enums import TimeUnit

class Time:

    def __init__(self, time_unit, value):
        self.__unit = time_unit
        self.__value = value

    @staticmethod
    def seconds(self, secs):
        return Time(TimeUnit.SECONDS, secs)

    @staticmethod
    def milli_seconds(self, ms):
        return Time(TimeUnit.MILLI_SECONDS, ms)

    @staticmethod
    def minutes(self, mins):
        return Time(TimeUnit.MINUTES, mins)

from arjuna.tpi import Arjuna

logger = Arjuna.get_logger()
console = Arjuna.get_console()

