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

    def _emd(self, *locators):
        return self._automator._create_lmd(*locators)

    def configure(self, config):
        self.impl.configure(config.settings)
        return self

class DefaultGuiElement(BaseComponent):

    def __init__(self, automator, impl, index=None):
        super().__init__(automator, GuiComponentType.ELEMENT, impl)
        self.__index = index
        # self.is_gom_element = impl.is_gom_element()

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

    def hover(self):
        self.impl.hover()

    def _emd(self, *locators):
        return self._automator._create_lmd(*locators)

    def element(self, *with_locators):
        return self.impl.define_element(self._emd(*with_locators))

    def multi_element(self, *with_locators):
        return self.impl.define_multielement(self._emd(*with_locators))

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
        return self.impl.has_value_selected(value)

    def has_index_selected(self, index):
        return self.impl.has_index_selected(index)

    def select_value(self, value):
        self.impl.select_by_value(value)

    def select_index(self, index):
        self.impl.select_by_index(index)

    @property
    def first_selected_option_value(self):
        return self.impl.get_first_selected_option_value()

class DefaultDropDown(MultiElementSelectable):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.DROPDOWN, impl)

    @property
    def _option_locators(self):
        pass

    @_option_locators.setter
    def option_locators(self, *with_locators):
        self.impl.set_option_locators(self.__emd(*with_locators))

    @property
    def _option_container(self):
        pass

    @_option_container.setter
    def option_container(self, *with_locators):
        self.impl.set_option_container(self.__emd(*with_locators))

    @property
    def first_selected_option_text(self):
        return self.impl.get_first_selected_option_text()

    def has_visible_text_selected(self, text):
        return self.impl.has_visible_text_selected(text)

    def select_visible_text(self, text):
        self.impl.select_by_visible_text(text)

    def send_option_text(self, text):
        self.impl.send_option_text(text)

class DefaultRadioGroup(MultiElementSelectable):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.RADIOGROUP, impl)

    def configure(self, config):
        pass

class DefaultAlert(BaseComponent):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.ALERT, impl)

    def confirm(self):
        self.impl.confirm()

    def dismiss(self):
        self.impl.dismiss()

    @property
    def text(self):
        return self.impl.get_text()

    def send_text(self, text):
        self.impl.send_text(text)


class DefaultBrowser(BaseComponent):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.BROWSER, impl)

    def go_to_url(self, url):
        self.impl.go_to_url(url)

    def go_back(self):
        self.impl.go_back()

    def go_forward(self):
        self.impl.go_forward()
        self._send_request(ArjunaComponent.GUI_AUTOMATOR, GuiAutoActionType.BROWSER_GO_FORWARD)

    def refresh(self):
        self.impl.refresh()

    @property
    def dom_root(self):
        return DefaultDomRoot(self._automator, self.impl.dom_root)

class BaseFrame(BaseComponent):

    def __init__(self, automator, comp_type, impl):
        super().__init__(automator, comp_type, impl)    
        
    def focus(self):
        self.impl.focus()

    def frame(self, *with_locators):
        return GuiAutoComponentFactory.Frame(self._automator, self.impl.define_frame(self._emd(*with_locators)))

    @property
    def parent(self):
        return GuiAutoComponentFactory.Frame(self._automator, self.impl.parent)

    def enumerate_frames(self):
        return self.impl.enumerate_frames()

class DefaultFrame(BaseFrame):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.FRAME, impl)

class DefaultDomRoot(BaseFrame):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.DOMROOT, impl)
    
    @property
    def parent(self):
        raise Exception("DOM root does not have a parent frame.")


class AbstractBasicWindow(BaseComponent):

    def __init__(self, automator, comp_type, impl):
        super().__init__(automator, comp_type, impl)

    @property
    def title(self):
        return self.impl.title

    def focus(self):
        self.impl.focus()


class DefaultChildWindow(AbstractBasicWindow):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.CHILD_WINDOW, impl)

    def close(self):
        self.impl.close()

    @property
    def main_window(self):
        self._automator.main_window


class DefaultMainWindow(AbstractBasicWindow):

    def __init__(self, automator, impl):
        super().__init__(automator, GuiComponentType.MAIN_WINDOW, impl)

    def maximize(self):
        self.impl.maximize()

    def _take_element_finding_action(self, setu_action_type, *setu_args):
        response = self._send_request(ArjunaComponent.GUI_AUTOMATOR, setu_action_type, *setu_args)
        return response.get_value_for_gui_component_setu_id()

    def child_window(self, *with_locators):
        win =  self.impl.define_child_window(self._emd(*with_locators))
        return DefaultChildWindow(self._automator, win)

    @property
    def latest_child_window(self):
        return DefaultChildWindow(self._automator, self.impl.get_latest_child_window())
 
    def close_all_child_windows(self):
        self.impl.close_all_child_windows()
