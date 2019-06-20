from .driverelement import SeleniumDriverElement
from arjuna.setuext.guiauto.dispatcher.driver.impl.driver_commands import DriverCommands
from arjuna.setuext.guiauto.dispatcher.driver.impl.element_finder import ElementFinder


class SeleniumDriver:

    def __init__(self, setu_id):
        self.__setu_id = setu_id
        self.__config = None
        self.__driver = None
        self.__driver_elements = {}
        self.__driver_melements = {}

    def create_gui_element_dispatcher(self, element_setu_id):
        return SeleniumDriverElement(self, element_setu_id)

    @property
    def setu_id(self):
        return self.__setu_id

    @property
    def driver(self):
        return self.__driver

    def add_driver_element(self, setu_id, element):
        self.__driver_elements[setu_id] = element

    def add_driver_melement(self, setu_id, melement):
        self.__driver_melements[setu_id] = melement

    def get_driver_element(self, setu_id):
        return self.__driver_elements[setu_id]

    def get_driver_melement(self, setu_id):
        return self.__driver_melements[setu_id]

    def __create_success_response(self):
        response = dict()
        response["result"] = "success"
        response["data"] = {}
        return response

    def launch(self, config):
        self.__config = config
        from .impl.browser_launcher import BrowserLauncher
        self.__driver = BrowserLauncher.launch(config) 

    def quit(self):
        DriverCommands.quit(self.__driver)

    def go_to_url(self, url):
        DriverCommands.go_to_url(self.__driver, url)

    def go_back_in_browser(self):
        DriverCommands.go_back_in_browser(self.__driver)

    def go_forward_in_browser(self):
        DriverCommands.go_forward_in_browser(self.__driver)

    def refersh_browser(self):
        DriverCommands.refersh_browser(self.__driver)

    def execute_javascript(self, script):
        DriverCommands.execute_javascript(self.__driver, script)

    def take_screenshot(self):
        DriverCommands.take_screenshot(self.__driver)

    def find_element(self, child_gui_element_setu_id, with_type, with_value):
        element = ElementFinder.find_element(self.__driver, with_type, with_value)
        self.__driver_elements[child_gui_element_setu_id] = element

    def find_multielement(self, child_gui_element_setu_id, with_type, with_value):
        melement = ElementFinder.find_elements(self.__driver, with_type, with_value)
        self.__driver_melements[child_gui_element_setu_id] = melement
        return melement.get_instance_count()

    def get_current_window_handle(self):
        return DriverCommands.get_current_window_handle(self.__driver)

    def get_current_window_title(self):
        return DriverCommands.get_window_title(self.__driver)

    def maximize_current_window(self):
        DriverCommands.maximize_window(self.__driver)

    def get_current_window_size(self):
        res = DriverCommands.get_current_window_size(self.__driver)
        return {"width" : res[0], "height" : res[1]}

    def get_all_window_handles(self):
        return DriverCommands.get_all_winodw_handles(self.__driver)

    def focus_on_window(self, handle):
        DriverCommands.focus_on_window(self.__driver, handle)

    def close_current_window(self):
        DriverCommands.close_current_window(self.__driver)

    def is_web_alert_present(self):
        return DriverCommands.is_web_alert_present(self.__driver)

    def confirm_web_alert(self):
        DriverCommands.confirm_web_alert(self.__driver)

    def dismiss_web_alert(self):
        DriverCommands.dismiss_web_alert(self.__driver)

    def get_text_from_web_alert(self):
        return DriverCommands.get_text_from_web_alert(self.__driver)

    def send_text_to_web_alert(self, text):
        DriverCommands.send_text_to_web_alert(self.__driver, text)

    def focus_on_frame(self, elem_setu_id, is_instance_action=False, instance_index=0):
        element = None
        if is_instance_action:
            element = self.__driver_melements[elem_setu_id].get_element_at_index(instance_index)
        else:
            element = self.__driver_elements[elem_setu_id]
        DriverCommands.focus_on_frame(self.__driver, element)

    def focus_on_parent_frame(self):
        DriverCommands.focus_on_parent_frame(self.__driver)

    def focus_on_dom_root(self):
        DriverCommands.focus_on_dom_root(self.__driver)
