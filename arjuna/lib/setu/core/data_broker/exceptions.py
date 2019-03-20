

class DataSourceFinished(StopIteration):
    def __init__(self, msg=None):
        super().__init__(msg is None and "Done" or msg)