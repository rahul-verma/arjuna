from arjuna.tpi.enums import ArjunaOption, SetuActorMode
from arjuna.setu.dispatcher.setu_actor_requester import SetuActorRequester
from arjuna.tpi.enums import GuiAutomatorName
from .element import GuiElementDispatcher
from functools import partial

class GuiAutomatorDispatcher:

    def __init__(self, config, setu_id):
        self.__config = config
        self.__setu_id = setu_id
        self.__dispatcher = None
        self.__automator_name = config.setu_config.get_gui_automator_name()
        self.__actor_mode = config.setu_config.get_guiauto_actor_mode()

        if self.__actor_mode == SetuActorMode.REMOTE:
            actor_url = config.setu_config.value(ArjunaOption.SETU_GUIAUTO_ACTOR_URL)
            if (self.__automator_name == GuiAutomatorName.SELENIUM):
                from arjuna.setuext.guiauto.dispatcher.selenium.remote.driver import SeleniumDriver
                self.__dispatcher = SeleniumDriver(setu_id, SetuActorRequester(actor_url))
            else:
                raise Exception("{} automator is not aupported.".format(self.__automator_name.name))
        else:
            if (self.__automator_name == GuiAutomatorName.SELENIUM):
                from arjuna.setuext.guiauto.dispatcher.selenium.local.driver import SeleniumDriver
                self.__dispatcher = SeleniumDriver(setu_id)
            else:
                raise Exception("{} automator is not aupported.".format(self.__automator_name.name))

    def create_gui_element_dispatacher(self, element_setu_id):
        return GuiElementDispatcher(
            self.__config,
            self.__automator_name,
            self.__dispatcher, 
            element_setu_id
        )

    def __getattr__(self, attr):
        return partial(vars(self.__dispatcher.__class__)[attr], self.__dispatcher)

    # Write __whatever__ override and check method delegation valid or not.