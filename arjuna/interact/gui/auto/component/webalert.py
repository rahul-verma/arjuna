from arjuna.interact.gui.auto.element.guielement import GuiElement
from arjuna.core.enums import ArjunaOption

class WebAlert:

    def __init__(self, automator):
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

    @property
    def text(self):
        return self.automator.dispatcher.get_text_from_web_alert()

    @text.setter
    def text(self, text):
        self.automator.dispatcher.send_text_to_web_alert(text)