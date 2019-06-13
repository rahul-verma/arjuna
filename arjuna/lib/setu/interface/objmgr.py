

class SetuSvcObjectManager:
    TESTSESSION_HANDLERS = {}

    @classmethod
    def register_testsession_handler(cls, handler):
        cls.TESTSESSION_HANDLERS[handler.setu_id] = handler

    @classmethod
    def deregister_testsession_handler(cls, handler):
        #cascading calls to all test handler objects needed.
        del cls.TESTSESSION_HANDLERS[handler.setu_id]

    @classmethod
    def get_testsession_handler(cls, setu_id):
        return cls.TESTSESSION_HANDLERS[setu_id]

    @classmethod
    def has_active_testsession(cls):
        return len(cls.TESTSESSION_HANDLERS) > 0

    @classmethod
    def deregister_all_existing_testsessions(cls):
        testsession_handles = tuple(cls.TESTSESSION_HANDLERS.values())
        for handler in testsession_handles:
            cls.deregister_testsession_handler(handler)

