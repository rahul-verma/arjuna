from functools import partial

class GuiElementDispatcher:

    def __init__(self, config, automator_name, automator_dispatcher, element_setu_id):
        self.__config = config
        self.__dispatcher = None

        self.__dispatcher = automator_dispatcher.create_gui_element_dispatcher(element_setu_id)

    def __getattr__(self, attr):
        return partial(vars(self.__dispatcher.__class__)[attr], self.__dispatcher)