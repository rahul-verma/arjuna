from enum import Enum, auto
from arjuna.client.core.action import *
from arjuna.client.core.config import ArjunaComponent
from arjuna.client.core.connector import BaseSetuObject, SetuArg
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
            self.__test_session = config.get_test_session()
            self._set_test_session_setu_id_arg(self.__test_session.get_setu_id())
            self.__config = config

    def _set_automation_context(self, context):
        self.__auto_context = context

    def get_automation_context(self):
        return self.__auto_context

    def is_gui(self):
        return False

    def __take_element_finder_action(self, setu_action_type, *setu_args):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, setu_action_type, *setu_args)
        return response.get_value_for_element_setu_id()

    def __create_generic_element(self, setu_action_type, *with_locators):
        if with_locators:
            locators = [l.as_map() for l in with_locators]
            return self.__take_element_finder_action(setu_action_type, SetuArg.arg("locators", locators))
        else:
            return self.__take_element_finder_action(setu_action_type)

    def Element(self, *with_locators):
        elem_setu_id = self.__create_generic_element(GuiAutoActionType.CREATE_ELEMENT, *with_locators)
        return GuiAutoComponentFactory.Element(self.__test_session, self, elem_setu_id)

    def MultiElement(self, *with_locators):
        elem_setu_id = self.__create_generic_element(GuiAutoActionType.CREATE_MULTIELEMENT, *with_locators)
        return GuiAutoComponentFactory.MultiElement(self.__test_session, self, elem_setu_id)

    def DropDown(self, *with_locators):
        elem_setu_id = self.__create_generic_element(GuiAutoActionType.CREATE_DROPDOWN, *with_locators)
        return GuiAutoComponentFactory.DropDown(self.__test_session, self, elem_setu_id)

    def RadioGroup(self, *with_locators):
        elem_setu_id = self.__create_generic_element(GuiAutoActionType.CREATE_RADIOGROUP, *with_locators)
        return GuiAutoComponentFactory.RadioGroup(self.__test_session, self, elem_setu_id)

    def Alert(self):
        elem_setu_id = self.__create_generic_element(GuiAutoActionType.CREATE_ALERT)
        return GuiAutoComponentFactory.Alert(self.__test_session, self, elem_setu_id)

    def Frame(self, *with_locators):
        return self.DomRoot().Frame(*with_locators)

    def ChildWindow(self, *with_locators):
        return self.MainWindow().ChildWindow(*with_locators)

    def LatestChildWindow(self):
        return self.MainWindow().LatestChildWindow()

    def close_all_child_windows(self):
        self.MainWindow().close_all_child_windows()

    def MainWindow(self):
        return self.__main_window

    def _set_main_window(self, window):
        self.__main_window = window

    def get_config(self):
        return self.__config

    def _set_config(self, config):
        self.__config = config

    def DomRoot(self):
        return self.__dom_root

    def _set_dom_root(self, root):
        self.__dom_root = root

    def get_test_session(self):
        return self.__test_session

    def Browser(self):
        return self.__browser

    def _set_browser(self, browser):
        self.__browser = browser

    def enable_slow_motion(self, on, interval=None):
        args = [SetuArg.arg("on", on)]
        if interval:
            args.append(SetuArg.arg("interval", interval))
        self._send_request(GuiAutoActionType.SET_SLOMO, *args)

    def execute_javascript(self, script):
        self._send_request(GuiAutoActionType.BROWSER_EXECUTE_JAVASCRIPT, SetuArg.arg("script", script))


class DefaultGuiAutomator(AbstractAppAutomator):

    def __init__(self, config, extendedConfig=None):
        super().__init__(config)
        self.__extended_config = extendedConfig
        self.__launch()

    def __launch(self):
        response = None
        if self.__extended_config:
            response = self._send_request(
                ArjunaComponent.GUI_AUTOMATOR,
                GuiAutoActionType.LAUNCH_AUTOMATOR,
                SetuArg.config_arg(self.get_config().get_setu_id()),
                SetuArg.arg("extendedConfig", self.__extended_config)
            )
        else:
            response = self._send_request(
                ArjunaComponent.GUI_AUTOMATOR,
                GuiAutoActionType.LAUNCH_AUTOMATOR,
                SetuArg.config_arg(self.get_config().get_setu_id())
            )

        self._set_setu_id(response.get_value_for_guiautomator_setu_id())
        self._set_self_setu_id_arg("automatorSetuId")

        win_response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DEFINE_MAIN_WINDOW)
        self._set_main_window(GuiAutoComponentFactory.MainWindow(self.get_test_session(), self, win_response.get_value_for_element_setu_id()))

        self._set_dom_root(GuiAutoComponentFactory.DomRoot(self.get_test_session(), self))
        self._set_browser(GuiAutoComponentFactory.Browser(self.get_test_session(), self))

    def quit(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.QUIT_AUTOMATOR)
