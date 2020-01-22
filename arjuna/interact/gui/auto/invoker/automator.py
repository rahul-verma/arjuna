from enum import Enum, auto
from arjuna.tpi.guiauto.helpers import With
from arjuna.interact.gui.auto.invoker.mkactions import *
from .component import GuiAutoComponentFactory

from arjuna.interact.gui.auto.impl.automator import GuiAutomator as ImplGuiAutomator
from arjuna.interact.gui.auto.invoker.source import DefaultGuiSource

class GuiAutomatorName(Enum):
    SELENIUM = auto()
    APPIUM = auto()

class GuiAutomator:

    def __init__(self, config=None, extended_config=None):
        from arjuna.tpi import Arjuna
        self.__config = config and config or Arjuna.get_ref_config()
        self.__test_session = self.config.test_session
        self.__dom_root = None
        self.__main_window = None
        self.__browser = None
        self.__auto_context = None
        self._set_impl_automator(ImplGuiAutomator(config, extended_config))
        self._set_main_window(GuiAutoComponentFactory.MainWindow(self, self.impl_automator.main_window))
        self._set_browser(GuiAutoComponentFactory.Browser(self, self.impl_automator.browser))

    def _set_impl_automator(self, automator):
        self.__impl_automator = automator

    @property
    def config(self):
        return self.__config

    @property
    def impl_automator(self):
        return self.__impl_automator

    def _set_automation_context(self, context):
        self.__auto_context = context

    @property
    def context(self):
        return self.__auto_context

    @property
    def test_session(self):
        return self.__test_session

    def is_gui(self):
        return False

    def _create_lmd(self, *locators):
        return self.impl_automator.create_lmd(*locators)

    def element(self, *with_locators):
        impl = self.impl_automator.define_element(self._create_lmd(*with_locators))
        return GuiAutoComponentFactory.Element(self, impl)

    def multi_element(self, *with_locators):
        impl = self.impl_automator.define_multielement(self._create_lmd(*with_locators))
        return GuiAutoComponentFactory.MultiElement(self, impl)

    def dropdown(self, *with_locators, option_container_locators=None, option_locators=None):
        def convert_to_tuple(in_data):
            if isinstance(in_data, With):
                return (in_data, )
            elif type(in_data) in {list, tuple}:
                return in_data
            else:
                raise Exception("Expected a With object or a list/tuple of With objects")
        impl = self.impl_automator.define_dropdown(
            self._create_lmd(*with_locators),
            option_container_lmd= option_container_locators and self._create_lmd(*convert_to_tuple(option_container_locators)) or None,
            option_lmd=option_locators and self._create_lmd(*convert_to_tuple(option_locators)) or None
        )
        return GuiAutoComponentFactory.DropDown(self, impl)

    def radio_group(self, *with_locators):
        impl = self.impl_automator.define_radiogroup(self._create_lmd(*with_locators))
        return GuiAutoComponentFactory.RadioGroup(self, impl)

    def frame(self, *with_locators):
        # Conversion takes place IFrame implementation for locator -> emd
        return self.dom_root.frame(*with_locators)

    def child_window(self, *with_locators):
        return self.main_window.child_window(*with_locators)

    def close_all_child_windows(self):
        self.main_window.close_all_child_windows()

    @property
    def alert(self):
        impl = self.impl_automator.alert_handler.create_alert()
        return GuiAutoComponentFactory.Alert(self, impl)

    @property
    def main_window(self):
        return self.__main_window

    def _set_main_window(self, window):
        self.__main_window = window

    @property
    def latest_child_window(self):
        return self.main_window.latest_child_window

    @property
    def config(self):
        return self.__config

    def _set_config(self, config):
        self.__config = config

    @property
    def dom_root(self):
        return self.browser.dom_root

    def _set_dom_root(self, root):
        self.__dom_root = root

    @property
    def test_session(self):
        return self.__test_session

    @property
    def browser(self):
        return self.__browser

    def _set_browser(self, browser):
        self.__browser = browser

    def enable_slow_motion(self, on, interval=None):
        args = [SetuArg.arg("on", on)]
        if interval:
            args.append(SetuArg.arg("interval", interval))
        self._send_request(GuiAutoActionType.SET_SLOMO, *args)

    def execute_javascript(self, script):
        return self.impl_automator.browser.execute_javascript(script)

    @property
    def source(self):
        return DefaultGuiSource(self, self.impl_automator.get_source())

    def new_action_chain(self):
        return SingleActionChain(self)

    def perform_composite_action(self):
        pass

    def quit(self):
        self.impl_automator.quit()
