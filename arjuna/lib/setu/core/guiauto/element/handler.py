import abc
import types

class Handler(metaclass=abc.ABCMeta):

    def __init__(self, element_obj):
        self.__element = element_obj
        self.__config = element_obj.config

    @property
    def element(self):
        return self.__element

    @property
    def config(self):
        return self.__config

    def _act(self, json_dict):
        return self.__element.actor_callable(json_dict)