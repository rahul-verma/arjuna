from .guiautomator import GuiAutomatorHandler

class Receiver:
    AUTOMATOR_HANDLERS = dict()

    @classmethod
    def create_gui_automator_dispatcher(cls, setu_id):
        handler = GuiAutomatorHandler(setu_id)
        cls.AUTOMATOR_HANDLERS[setu_id] = handler
        return handler

    @classmethod
    def create_gui_element_dispatcher(cls, automator_setu_id, element_setu_id):
        handler = cls.AUTOMATOR_HANDLERS[automator_setu_id]
        return handler.create_gui_element_handler(element_setu_id)


    