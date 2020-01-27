from .gui import *

class Page(AppPortion):

    def __init__(self, app, automator, *, label=None):
        super().__init__(app, automator, label=label)

class Widget(AppPortion):

    def __init__(self, page, *, label=None):
        super().__init__(page.app, page._automator, label=label)    

    @property
    def page(self):
        return self.__page


class App(Gui, metaclass=abc.ABCMeta):

    def __init__(self, *, config=None, ext_config=None, label=None, ns_dir=None):
        super().__init__(config=config, ext_config=ext_config, label=label)
        self.__ui = None
        self.__automator = None
        self.__ns_dir = ns_dir

    @property
    def _automator(self):
        return self.__automator

    @property
    def ns_dir(self):
        return self.__ns_dir

    def _launch_automator(self):
        # Default Gui automation engine is Selenium
        from arjuna.interact.gui.auto.automator import GuiAutomator
        self.__automator = GuiAutomator(self.config, self.ext_config)

    @property
    def ui(self):
        return self.__ui

    def _create_default_ui(self):
        self.__ui = Page(self, self._automator, label="{}-Def-UI".format(self.label))

    @abc.abstractmethod
    def launch(self):
        pass

class WebApp(App):

    def __init__(self, *, base_url=None, blank_slate=False, config=None, ext_config=None, label=None, ns_dir=None):
        '''
            Creates and returns GuiAutomator object for provided config.
            If no configuration is provided reference configuration is used.
            You can also provide GuiDriverExtendedConfig for extended configuration for WebDriver family of libs. 
        '''
        super().__init__(config=config, ext_config=ext_config, label=label, ns_dir=ns_dir)
        from arjuna.tpi.enums import ArjunaOption
        self.__base_url = base_url is not None and base_url or self.config.get_arjuna_option_value(ArjunaOption.AUT_BASE_URL).as_str()

    @property
    def base_url(self):
        return self.__base_url

    def launch(self, blank_slate=False):
        self._launch_automator()
        if not blank_slate:
            self._automator.browser.go_to_url(self.base_url)
        self._create_default_ui()

    def quit(self):
        self._automator.quit()