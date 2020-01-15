from enum import Enum, auto
import random

from arjuna.interact.gui.auto.invoker.source import DefaultGuiSource

class GuiComponentType(Enum):
    ELEMENT = auto()
    MULTI_ELEMENT = auto()
    DROPDOWN = auto()
    RADIOGROUP = auto()
    BROWSER = auto()
    DOMROOT = auto()
    FRAME = auto()
    WINDOW = auto()
    MAIN_WINDOW = auto()
    CHILD_WINDOW = auto()
    ALERT = auto()

class GuiAutoComponentFactory:

    @staticmethod
    def Element(automator, impl_element):
        return DefaultGuiElement(automator, impl_element)

    @staticmethod
    def MultiElement(automator, impl_melement):
        return DefaultGuiMultiElement(automator, impl_melement)

    @staticmethod
    def DropDown(automator, impl_dropdown):
        return DefaultDropDown(automator, impl_dropdown)

    @staticmethod
    def RadioGroup(automator, impl_radiogroup):
        return DefaultRadioGroup(automator, impl_radiogroup)

    @staticmethod
    def Alert(automator, impl_alert):
        return DefaultAlert(automator, impl_alert)

    @staticmethod
    def MainWindow(automator, impl_main_window):
        return DefaultMainWindow(automator, impl_main_window)

    @staticmethod
    def DomRoot(automator, impl_dom_root):
        return DefaultDomRoot(automator, impl_dom_root)

    @staticmethod
    def Frame(automator, impl_frame):
        return DefaultFrame(automator, impl_frame)

    @staticmethod
    def Browser(automator, impl_browser):
        return DefaultBrowser(automator, impl_browser)


class BaseComponent:

    def __init__(self, automator, component_type, impl_component):
        super().__init__()
        self.__automator = automator
        self.__comp_type = component_type
        self.__impl_component = impl_component

    @property
    def _automator(self):
        return self.__automator

    @property
    def _test_session(self):
        return self.automator.test_session

    @property
    def component_type(self):
        return self.__comp_type

    @property
    def impl(self):
        return self.__impl_component

    @property
    def source(self):
        return DefaultGuiSource(self._automator, self.impl.get_source())

class DefaultGuiElement(BaseComponent):

    def __init__(self, automator, impl, index=None):
        super().__init__(automator, GuiComponentType.ELEMENT, impl)
        self.__index = index

    def enter_text(self, text):
        self.impl.enter_text(text)

    def set_text(self, text):
        self.impl.set_text(text)

    def click(self):
        self.impl.click()

    def wait_until_present(self):
        self.impl.wait_until_present()

    def wait_until_visible(self):
        self.impl.wait_until_visible()

    def wait_until_clickable(self):
        self.impl.wait_until_clickable()

    def check(self):
        self.impl.check()

    def uncheck(self):
        self.impl.uncheck()

    def identify(self):
        self.impl.identify()

    def configure(self, config):
        self.impl.configure(config)
        return self

class DefaultGuiMultiElement(BaseComponent):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.ELEMENT, impl)

    def at_index(self, index):
        return DefaultGuiElement(self._automator, self.impl.get_instance_at_index(index), index)

    @property
    def first(self):
        return self.at_index(0)

    @property
    def last(self):
        return self.at_index(self.length -1)

    @property
    def random(self):
        return self.at_index(random.randint(0, self.length-1))

    @property
    def length(self):
        return self.impl.get_instance_count()

class MultiElementSelectable(BaseComponent):

    def __init__(self, automator, comp_type, impl):
        super().__init__(automator, comp_type, impl)

    def has_value_selected(self, value):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_HAS_VALUE_SELECTED, SetuArg.value_arg(value))
        return response.get_value_for_check_result()

    def has_index_selected(self, index):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_HAS_INDEX_SELECTED, SetuArg.index_arg(index))
        return response.get_value_for_check_result()

    def select_by_value(self, value):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_SELECT_BY_VALUE, SetuArg.value_arg(value))

    def select_by_index(self, index):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_SELECT_BY_INDEX, SetuArg.index_arg(index))

    def get_first_selected_option_value(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_VALUE)
        return response.get_value_for_value_attr()

class DefaultDropDown(MultiElementSelectable):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.DROPDOWN, impl)

    def configure(self):
        pass

    def set_option_locators(self, *with_locators):
        pass

    def set_option_container(self, *with_locators):
        pass

    def get_first_selected_option_text(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_GET_FIRST_SELECTED_OPTION_TEXT)
        return response.get_value_for_text()

    def has_visible_text_selected(self, text):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_HAS_VISIBLE_TEXT_SELECTED, SetuArg.text_arg(text))
        return response.get_value_for_check_result()

    def select_by_visible_text(self, text):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DROPDOWN_SELECT_BY_VISIBLE_TEXT, SetuArg.text_arg(text))


class DefaultRadioGroup(MultiElementSelectable):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.RADIOGROUP, impl)

    def configure(self, config):
        pass

class DefaultAlert(BaseComponent):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.ALERT, impl)

    def confirm(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_CONFIRM)

    def dismiss(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_DISMISS)

    def get_text(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_GET_TEXT)
        return response.get_value_for_text()

    def send_text(self, text):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.ALERT_SEND_TEXT, SetuArg.text_arg(text))


class DefaultBrowser(BaseComponent):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.BROWSER, impl)

    def go_to_url(self, url):
        self.impl.go_to_url(url)

    def go_back(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_GO_BACK)

    def go_forward(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_GO_FORWARD)

    def refresh(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_REFRESH)

class BaseFrame(BaseComponent):

    def __init__(self, automator, comp_type, impl):
        super().__init__(automator, comp_type, impl)

    def focus(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.FRAME_FOCUS)

    def Frame(self, *withLocators):
        pass

    def ParentFrame(self):
        pass

    def enumerateFrames(self):
        pass

class DefaultFrame(BaseFrame):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.FRAME, impl)

class DefaultDomRoot(BaseFrame):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.DOMROOT, impl)

    def focus(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.DOMROOT_FOCUS)

    def Frame(self, *with_locators):
        pass
    
    def ParentFrame(self):
        raise Exception("DOM root does not have a parent frame.")


class AbstractBasicWindow(BaseComponent):

    def __init__(self, automator, comp_type, impl):
        super().__init__(automator, comp_type, impl)

    @property
    def title(self):
        return self.impl.title

    def focus(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.WINDOW_FOCUS)


class DefaultChildWindow(AbstractBasicWindow):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.CHILD_WINDOW, impl)

    def close(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.CHILD_WINDOW_CLOSE)

    def MainWindow(self):
        return self._get_automator().MainWindow()


class DefaultMainWindow(AbstractBasicWindow):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.MAIN_WINDOW, impl)

    def maximize(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_MAXIMIZE)

    def _take_element_finding_action(self, setu_action_type, *setu_args):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, setu_action_type, *setu_args)
        return response.get_value_for_gui_component_setu_id()

    def ChildWindow(self, *withLocators):
        arg = [l.asMap() for l in withLocators]
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_CREATE_CHILD_WINDOW, SetuArg.arg("locators", arg))
        return DefaultChildWindow(self._get_test_session(), self._get_automator(), response.get_value_for_gui_component_setu_id())

    def LatestChildWindow(self):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_GET_LATEST_CHILD_WINDOW)
        return DefaultChildWindow(self._get_test_session(), self._get_automator(), response.get_value_for_gui_component_setu_id())

    def close_all_child_windows(self):
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.MAIN_WINDOW_CLOSE_ALL_CHILD_WINDOWS)
