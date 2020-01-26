from arjuna.core.enums import GuiActionConfigType

class Configurable:

    def __init__(self, automator):
        self.__settings = {
            GuiActionConfigType.CHECK_TYPE: True,
            GuiActionConfigType.CHECK_PRE_STATE : True,
            GuiActionConfigType.CHECK_POST_STATE : True,
    }

    @property
    def settings(self):
        return self.__settings

    def configure(self, settings):
        self.__settings.update(settings)

    def _should_check_type(self):
        return self.settings[GuiActionConfigType.CHECK_TYPE]

    def _should_check_pre_state(self):
        return self.settings[GuiActionConfigType.CHECK_PRE_STATE]

    def _should_check_post_state(self):
        return self.settings[GuiActionConfigType.CHECK_POST_STATE]