from arjuna.tpi.enums import ArjunaOption

from .guiautomator import GuiAutomator
from .handler import Handler

class Browser(Handler):

    def __init__(self, automator: GuiAutomator):
        super().__init__(automator)
        from arjuna.setuext.guiauto.impl.element.frame import DomRoot
        self.__dom_root = DomRoot(automator)

    @property
    def dom_root(self):
        return self.__dom_root

    def go_to_url(self, url):
        self.automator.dispatcher.go_to_url(url=url)

    def go_back(self, url):
        self.automator.dispatcher.go_back()

    def go_forward(self, url):
        self.automator.dispatcher.go_forward()

    def refresh(self, url):
        self.automator.dispatcher.refresh()

    def execute_javascript(self, js):
        self.automator.dispatcher.execute_javascript(script=js)