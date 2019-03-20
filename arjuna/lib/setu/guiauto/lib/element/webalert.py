from arjuna.lib.setu.core.lib.setu_types import SetuManagedObject
from arjuna.lib.setu.guiauto.lib.element.guielement import GuiElement
from arjuna.lib.setu.core.constants import SetuConfigOption

class WebAlert(SetuManagedObject):

    def __init__(self, automator):
        super().__init__()
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def confirm(self):
        self.automator.dispatcher.confirm_web_alert()
        self.automator.alert_handler.delete_alert()

    def dismiss(self):
        self.automator.dispatcher.dismiss_web_alert()
        self.automator.alert_handler.delete_alert()

    def send_text(self, text):
        self.automator.dispatcher.send_text_to_web_alert(text)

    def get_text(self):
        return self.automator.dispatcher.get_text_from_web_alert()