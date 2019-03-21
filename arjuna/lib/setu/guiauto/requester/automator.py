from enum import Enum, auto
from arjuna.lib.setu.core.requester.config import SetuActionType, SetuArg
from arjuna.lib.setu.core.requester.connector import BaseSetuObject
from .component import GuiAutoComponentFactory

class GuiAutomatorName(Enum):
    SELENIUM = auto()
    APPIUM = auto()


class AbstractAppAutomator(BaseSetuObject):

    def __init__(self, config=None):
        super().__init__()
        self.__dom_root = None
        self.__main_window = None
        self.__browser = None
        self.__auto_context = None
        self.__test_session = None
        self.__config = None
        if config:
            self._set_config(config)
            self.__test_session = config.getTestSession()
            self._set_test_session_setu_id_arg(self.__test_session.getSetuId())
            self.__config = config

    def _set_automation_context(self, context):
        self.__auto_context = context

    def getAutomationContext(self):
        return self.__auto_context

    def isGui(self):
        return False

    def __take_element_finder_action(self, setu_action_type, *setu_args):
        response = self._send_request(setu_action_type, *setu_args)
        return response.getValueForElementSetuId()

    def __create_generic_element(self, setu_action_type, *withlocators):
        arg = [l.asMap() for l in withlocators]
        return self.__take_element_finder_action(setu_action_type, *arg)

    def elememt(self, *locators):
        elem_setu_id = self.__create_generic_element(SetuActionType.GUIAUTO_CREATE_ELEMENT, locators)
        return GuiAutoComponentFactory.Element(self.__test_session, self, elem_setu_id)

    def multiElement(self, *locators):
        elem_setu_id = self.__create_generic_element(SetuActionType.GUIAUTO_CREATE_MULTIELEMENT, locators)
        return GuiAutoComponentFactory.MultiElement(self.__test_session, self, elem_setu_id)

    def dropdown(self, *locators):
        elem_setu_id = self.__create_generic_element(SetuActionType.GUIAUTO_CREATE_DROPDOWN, locators)
        return GuiAutoComponentFactory.DropDown(self.__test_session, self, elem_setu_id)

    def radioGroup(self, *locators):
        elem_setu_id = self.__create_generic_element(SetuActionType.GUIAUTO_CREATE_RADIOGROUP, locators)
        return GuiAutoComponentFactory.RadioGroup(self.__test_session, self, elem_setu_id)

    def alert(self, *locators):
        elem_setu_id = self.__create_generic_element(SetuActionType.GUIAUTO_CREATE_ALERT, locators)
        return GuiAutoComponentFactory.Alert(self.__test_session, self, elem_setu_id)

    def frame(self, *locators):
        return self.domRoot().frame(locators)

    def childWindow(self, *locators):
        return self.mainWindow().childWindow(locators)

    def latestChildWindow(self):
        return self.mainWindow.latestChildWindow()

    def closeAllChildWindows(self):
        self.mainWindow.closeAllChildWindows()

    def mainWindow(self):
        return self.__main_window

    def _set_main_window(self, window):
        self.__main_window = window

    def getConfig(self):
        return self.__config

    def _set_config(self, config):
        self.__config = config

    def domRoot(self):
        return self.__dom_root

    def _set_dom_root(self, root):
        self.__dom_root = root

    def getTestSession(self):
        return self.__test_session

    def browser(self):
        return self.__browser

    def _set_browser(self, browser):
        self.__browser = browser

    def enableSlowMotion(self, on, interval=None):
        args = [SetuArg.arg("on", on)]
        if interval:
            args.append(SetuArg.arg("interval", interval)
        self._send_request(SetuActionType.GUIAUTO_SET_SLOMO, *args)

    def executeJavaScript(self, script):
        self._send_request(SetuActionType.GUIAUTO_BROWSER_EXECUTE_JAVASCRIPT, SetuArg.arg("script", script))


class DefaultGuiAutomator(AbstractAppAutomator):

    def __init__(self, config, extendedConfig=None):
        super().__init__(config)
        self.__extended_config = extendedConfig
        self.__launch()

    def __launch(self):
        response = None
        if self.__extended_config:
            response = self._send_request(
                SetuActionType.TESTSESSION_LAUNCH_GUIAUTOMATOR,
                SetuArg.configArg(self.getConfig().getSetuId()),
                SetuArg.arg("extendedConfig", self.__extended_config)
            )
        else:
            response = self._send_request(
                SetuActionType.TESTSESSION_LAUNCH_GUIAUTOMATOR,
                SetuArg.configArg(self.getConfig().getSetuId())
            )

        self.setSetuId(response.getValueForGuiAutomatorSetuId())
        self.setSelfSetuIdArg("automatorSetuId")

        win_response = self._send_request(SetuActionType.GUIAUTO_GET_MAIN_WINDOW)
        self.setMainWindow(GuiAutoComponentFactory.MainWindow(self.getTestSession(), self, win_response.getValueForElementSetuId()))

        self.setDomRoot(GuiAutoComponentFactory.DomRoot(self.getTestSession(), self))
        self.setBrowser(GuiAutoComponentFactory.Browser(self.getTestSession(), self))

    def quit(self):
        self._send_request(SetuActionType.TESTSESSION_QUIT_GUIAUTOMATOR)
