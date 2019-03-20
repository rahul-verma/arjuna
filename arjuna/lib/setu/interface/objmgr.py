

class SetuSvcObjectManager:
    TESTSESSION_HANDLERS = {}

    @classmethod
    def register_testsession_handler(cls, handler):
        cls.TESTSESSION_HANDLERS[handler.setu_id] = handler

    @classmethod
    def deregister_testsession_handler(cls, handler):
        del cls.TESTSESSION_HANDLERS[handler.setu_id]

    @classmethod
    def get_testsession_handler(cls, setu_id):
        return cls.TESTSESSION_HANDLERS[setu_id]

