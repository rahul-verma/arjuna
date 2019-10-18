import uuid
import abc
import types

class SetuManagedObject:

    def __init__(self, obj_name=""):
        self.__obj_name = obj_name
        self.__setu_id = str(uuid.uuid4())

    @property
    def setu_id(self):
        return self.__setu_id

    @property
    def obj_name(self):
        return self.__obj_name

    def get_setu_id(self):
        return self.__setu_id

class SetuConfiguredObject(SetuManagedObject, metaclass=abc.ABCMeta):

    def __init__(self, config, obj_name=""):
        super().__init__(obj_name)
        self.__dispatcher_creator = None
        self.__dispatcher = None
        self.__config = config

    @property
    def config(self):
        return self.__config

    @property
    def dispatcher(self):
        return self.__dispatcher

    def _set_dispatcher(self, dispatcher):
        self.__dispatcher = dispatcher

    @property
    def dispatcher_creator(self):
        return self.__dispatcher_creator

    @dispatcher_creator.setter
    def dispatcher_creator(self, creator):
        self.__dispatcher_creator = creator
        self.create_dispatcher()

    @abc.abstractmethod
    def create_dispatcher(self):
        pass