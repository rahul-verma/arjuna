from arjuna.core.adv.types import CIStringDict

class PipeLine:

    def __init__(self):
        self.__queue = list()

    def pop(self):
        try:
            return self.__queue.pop(0)
        except IndexError as e:
            raise Exception("Pipe line is empty.")

    def push(self, *values):
        self.__queue.extend(values)

    @property
    def length(self):
        return len(self.__queue)

class PipeLines(CIStringDict):

    def __init__(self):
        super().__init__()

    def create_pipeline(self, name):
        self[name] = PipeLine()
        return self[name]

class SharedObjects(CIStringDict):

    def __init__(self):
        super().__init__()

    def create_object(self, name, obj):
        self[name] = obj

class DataStore:

    def __init__(self):
        self.__store = {
            "pipelines" : PipeLines(),
            "shared_objects" : SharedObjects()
        }

    @property
    def pipelines(self):
        return self.__store["pipelines"]

    @property
    def shared_objects(self):
        return self.__store["shared_objects"]

    def create_pipeline(self, name):
        return self.pipelines.create_pipeline(name)

    def get_pipeline(self, name):
        return self.pipelines[name]

    def store_shared_object(self, name, obj):
        self.shared_objects.create_object(name, obj)

    def get_shared_object(self, name):
        return self.shared_objects[name]