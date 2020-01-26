

class Dispatchable:

    def __init__(self):
        self.__dispatcher = None

    @property
    def dispatcher(self):
        return self.__dispatcher

    @dispatcher.setter
    def dispatcher(self, dispatcher):
        self.__dispatcher = dispatcher