class DynamicCaller:

    def __init__(self, kallable, *args, **kwargs):
        self.__kallable = kallable
        self.__args = args
        self.__kwargs = kwargs

    def call(self):
        return self.__kallable(*self.__args, **self.__kwargs)