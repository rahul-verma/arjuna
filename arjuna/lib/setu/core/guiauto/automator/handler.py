import abc
import types
from .guiautomator import GuiAutomator

class Handler(metaclass=abc.ABCMeta):

    def __init__(self, automator: GuiAutomator):
        self.__automator = automator
        self.__config = automator.config

    @property
    def automator(self):
        return self.__automator

    @property
    def config(self):
        return self.__config

    def _act(self, json_dict):
        return self.automator.actor_callable(json_dict)