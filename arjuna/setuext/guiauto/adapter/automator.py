import uuid
from arjuna.setuext.guiauto.impl.automator.guiautomator import GuiAutomator
from arjuna.setuext.guiauto.impl.locator.emd import GuiElementMetaData
from arjuna.setu.adapter import Handler
from arjuna.client.core.action import *
from .action_map import *

# Arg names of methods show JSON names, so don't follow Python conventions.
class GuiAutomatorHandler(Handler):

    def __init__(self, dispatcher_creator):
        self.__dispatcher_creator = dispatcher_creator
        self.__automator = None

    def launch_automator(self, config, extendedConfig=None):
        self.__automator = GuiAutomator(config, extendedConfig)
        self.__automator.dispatcher_creator = self.__dispatcher_creator
        self.__automator.launch()

    def take_action(self, action_type, json_args):
        action_id = HANDLER_MAP[action_type]
        method_name, replaceable = HANDLER_NAME_MAP[action_id]
        return getattr(self, method_name)(action_type.name.replace(replaceable, "").lower(), json_args)

    def take_direct_action(self, action, json_args):
        return getattr(self, action)(**json_args)

    @property
    def setu_id(self):
        return self.automator.setu_id

    @property
    def automator(self):
        return self.__automator

    def quit_automator(self):
        self.automator.quit()

    def define_element(self, locators):
        elem = self.automator.create_element(GuiElementMetaData.createEMD(locators))
        return {"elementSetuId" : elem.setu_id}

    def define_element_with_emd(self, emd):
        elem = self.automator.create_element(emd)
        return {"elementSetuId" : elem.setu_id}

    def define_multielement(self, locators):
        elem = self.automator.create_multielement(GuiElementMetaData.createEMD(locators))
        return {"elementSetuId" : elem.setu_id}

    def define_multielement_with_emd(self, emd):
        elem = self.automator.create_multielement(emd)
        return {"elementSetuId" : elem.setu_id}

    def define_dropdown(self, locators):
        dropdown = self.automator.create_dropdown(GuiElementMetaData.createEMD(locators))
        return {"elementSetuId" : dropdown.setu_id}

    def define_dropdown_with_emd(self, emd):
        dropdown = self.automator.create_dropdown(emd)
        return {"elementSetuId" : dropdown.setu_id}

    def define_radiogroup(self, locators):
        radiogroup = self.automator.create_radiogroup(GuiElementMetaData.createEMD(locators))
        return {"elementSetuId" : radiogroup.setu_id}

    def define_radiogroup_with_emd(self, emd):
        radiogroup = self.automator.create_radiogroup(emd)
        return {"elementSetuId" : radiogroup.setu_id}

    def define_alert(self):
        alert = self.automator.alert_handler.create_alert()
        return {"elementSetuId" : alert.setu_id}

    def define_main_window(self):
        return {"elementSetuId" : self.automator.main_window.setu_id}

    def set_slomo(self, on, interval=None):
        self.automator.set_slomo(on, None)

    def take_window_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        win =  self.automator.main_window.get_window_for_setu_id(elem_setu_id)
        return getattr(WindowHandler, action)(win, **json_dict)

    def take_main_window_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        self.automator.slomo()
        win =  self.automator.main_window.get_window_for_setu_id(elem_setu_id)
        if not win.is_main_window():
            raise Exception("Window represented by {} is not the main window.".format(elem_setu_id))
        return getattr(MainWindowHandler, action)(self.automator.main_window, **json_dict)

    def take_child_window_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        self.automator.slomo()
        win =  self.automator.main_window.get_window_for_setu_id(elem_setu_id)
        return getattr(ChildWindowHandler, action)(win, **json_dict)

    def take_browser_action(self, action, json_dict):
        self.automator.slomo()
        return getattr(BrowserHandler, action)(self.automator.browser, **json_dict)

    def take_element_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        self.automator.slomo()
        instance_action = False
        if "isInstanceAction" in json_dict:
            instance_action = json_dict["isInstanceAction"]
            del json_dict["isInstanceAction"]
        if instance_action:
            index = json_dict["instanceIndex"]
            del json_dict["instanceIndex"]
            multi_element =  self.automator.get_multielement_for_setu_id(elem_setu_id)
            element = multi_element.get_instance_at_index(index)
        else:
            element =  self.automator.get_element_for_setu_id(elem_setu_id)
        return getattr(ElementHandler, action)(element, **json_dict)

    def take_multielement_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        multi_element =  self.automator.get_multielement_for_setu_id(elem_setu_id)
        return getattr(MultiElementHandler, action)(multi_element, **json_dict)

    def take_dropdown_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        self.automator.slomo()
        dropdown =  self.automator.get_element_for_setu_id(elem_setu_id)
        return getattr(DropdownHandler, action)(dropdown, **json_dict)

    def take_radiogroup_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        self.automator.slomo()
        radiogroup =  self.automator.get_element_for_setu_id(elem_setu_id)
        return getattr(RadioGroupHandler, action)(radiogroup, **json_dict)

    def take_alert_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        self.automator.slomo()
        alert =  self.automator.alert_handler.get_alert_for_setu_id(elem_setu_id)
        return getattr(AlertHandler, action)(alert, **json_dict)

    def take_domroot_action(self, action, json_dict):
        return getattr(DomRootHandler, action)(self.automator.browser.dom_root, **json_dict) 

    def create_frame_with_emd(self, emd):
        return self.take_domroot_action("create_frame_with_emd", {'emd':emd})

    def take_frame_action(self, action, json_dict):
        elem_setu_id = self.get_element_setuid(json_dict)
        frame =  self.automator.get_element_for_setu_id(elem_setu_id)
        return getattr(FrameHandler, action)(frame, **json_dict)


# Separates the underlying structure and names
# Also builds json response data where applicable
class ElementHandler:

    @classmethod
    def enter_text(cls, element, text):
        element.enter_text(text)

    @classmethod
    def set_text(cls, element, text):
        element.set_text(text)

    @classmethod
    def click(cls, element):
        element.click()

    @classmethod
    def check(cls, element):
        element.check()

    @classmethod
    def uncheck(cls, element):
        element.uncheck()

    @classmethod
    def wait_until_clickable(cls, element):
        element.wait_until_clickable()

class MultiElementHandler:
    pass

class DropdownHandler:

    @classmethod
    def has_visible_text_selected(cls, dropdown, text):
        return {"checkResult" : dropdown.has_visible_text_selected(text)}

    @classmethod
    def has_value_selected(cls, dropdown, value):
        return {"checkResult" : dropdown.has_value_selected(value)}

    @classmethod
    def has_index_selected(cls, dropdown, index):
        return {"checkResult" : dropdown.has_index_selected(index)}

    @classmethod
    def get_first_selected_option_text(cls, dropdown):
        return {"text" : dropdown.get_first_selected_option_text()}

    @classmethod
    def select_by_visible_text(cls, dropdown, text):
        return dropdown.select_by_visible_text(text)

    @classmethod
    def select_by_value(cls, dropdown, value):
        return dropdown.select_by_value(value)

    @classmethod
    def select_by_index(cls, dropdown, index):
        return dropdown.select_by_index(index)

class RadioGroupHandler:

    @classmethod
    def has_visible_text_selected(cls, radiogroup, text):
        return {"checkResult" : radiogroup.has_visible_text_selected(text)}

    @classmethod
    def has_value_selected(cls, radiogroup, value):
        return {"checkResult" : radiogroup.has_value_selected(value)}

    @classmethod
    def has_index_selected(cls, radiogroup, index):
        return {"checkResult" : radiogroup.has_index_selected(index)}

    @classmethod
    def get_first_selected_option_value(cls, radiogroup):
        return {"value" : radiogroup.get_first_selected_option_value()}

    @classmethod
    def select_by_value(cls, radiogroup, value):
        return radiogroup.select_by_value(value)

    @classmethod
    def select_by_index(cls, radiogroup, index):
        return radiogroup.select_by_index(index)

class WindowHandler:

    @classmethod
    def focus(cls, window):
        return window.focus()

    @classmethod
    def get_title(cls, window):
        return {"title" : window.get_title()}

class MainWindowHandler:

    @classmethod
    def maximize(cls, window):
        return window.maximize()

    @classmethod
    def close_all_child_windows(self, window):
        window.close_all_child_windows() 

    @classmethod
    def get_latest_child_window(self, window):
        return {"elementSetuId" : window.get_latest_child_window().setu_id}

class ChildWindowHandler:

    @classmethod
    def close(cls, window):
        return window.close()

class AlertHandler:

    @classmethod
    def confirm(cls, alert):
        alert.confirm()

    @classmethod
    def dismiss(cls, alert):
        alert.dismiss()

    @classmethod
    def get_text(cls, alert):
        return {"text" : alert.get_text()}

    @classmethod
    def send_text(cls, alert, text):
        alert.send_text(text)

class BrowserHandler:

    @classmethod
    def go_to_url(cls, browser, url):
       browser.go_to_url(url)

    @classmethod
    def go_back(cls, browser):
        browser.go_back()

    @classmethod
    def go_forward(cls, browser):
        browser.go_forward()

    @classmethod
    def refersh(cls, browser):
        browser.refersh()

    @classmethod
    def execute_javascript(self, browser, script):
        browser.execute_javascript(script) 

class DomRootHandler:

    @classmethod
    def focus(cls, dom_root):
        return dom_root.focus()

    @classmethod
    def create_frame(cls, dom_root, locators):
        return {"elementSetuId" : dom_root.create_frame(GuiElementMetaData.createEMD(locators)).setu_id}

    @classmethod
    def create_frame_with_emd(self, dom_root, emd):
        return {"elementSetuId" : dom_root.create_frame(emd).setu_id}

class FrameHandler:

    @classmethod
    def focus(cls, frame):
        return frame.focus()

    @classmethod
    def get_parent(cls, frame):
        return {"elementSetuId" : frame.get_parent().setu_id}

    @classmethod
    def create_frame(cls, frame, locators):
        return {"elementSetuId" : frame.create_frame(GuiElementMetaData.createEMD(locators)).setu_id}