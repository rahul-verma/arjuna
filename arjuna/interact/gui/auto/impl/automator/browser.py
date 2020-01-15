from arjuna.tpi.enums import ArjunaOption

class Browser:

    def __init__(self, automator):
        self.__automator = automator
        from arjuna.interact.gui.auto.impl.element.frame import DomRoot
        self.__dom_root = DomRoot(automator)

    @property
    def automator(self):
        return self.__automator

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