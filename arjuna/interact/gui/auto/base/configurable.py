from arjuna.core.enums import GuiInteractionConfigType

class Configurable:

    def __init__(self, gui, iconfig=None):
        self.__settings = {
            GuiInteractionConfigType.CHECK_TYPE: True,
            GuiInteractionConfigType.CHECK_PRE_STATE : True,
            GuiInteractionConfigType.CHECK_POST_STATE : True,
        }

        if iconfig:
            iconfig = type(iconfig) is dict and iconfig or iconfig.settings
            self.__settings.update(iconfig)

    @property
    def settings(self):
        return self.__settings

    def _should_check_type(self):
        return self.settings[GuiInteractionConfigType.CHECK_TYPE]

    def _should_check_pre_state(self):
        return self.settings[GuiInteractionConfigType.CHECK_PRE_STATE]

    def _should_check_post_state(self):
        return self.settings[GuiInteractionConfigType.CHECK_POST_STATE]