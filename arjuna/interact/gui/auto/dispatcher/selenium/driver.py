from .driverelement import SeleniumDriverElementDispatcher
from arjuna.interact.gui.auto.dispatcher.driver.driver_commands import DriverCommands
from arjuna.interact.gui.auto.dispatcher.driver.element_finder import ElementFinder
from arjuna.interact.gui.auto.dispatcher.driver.melement import MultiElement
from selenium.webdriver.remote.webelement import WebElement

class SeleniumDriverDispatcher:

    def __init__(self):
        self.__config = None
        self.__driver = None

    def __create_gui_element_dispatcher(self, element):
        return SeleniumDriverElementDispatcher.create_dispatcher(self, element)

    @property
    def driver(self):
        return self.__driver

    def launch(self, config):
        self.__config = config
        from .browser_launcher import BrowserLauncher
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

    def get_source(self):
        return DriverCommands.get_source(self.__driver)

    def execute_javascript(self, script):
        return DriverCommands.execute_javascript(self.__driver, script)

    def take_screenshot(self):
        DriverCommands.take_screenshot(self.__driver)

    def find_element(self, with_type, with_value):
        element = ElementFinder.find_element(self.__driver, with_type, with_value)
        return 1, self.__create_gui_element_dispatcher(element)

    def __process_single_js_element(self, element):
        # JS returns null, undefined
        if element is None:
            raise Exception("JavaScript could not find element.")
        elif not isinstance(element, WebElement):
            raise Exception("JavaScript returned a non-element object.")
        else:
            return element

    def __process_js_element_list(self, elements):
        if not elements: raise Exception("JavaScript could not find element.")
        return [self.__process_single_js_element(e) for e in elements]

    def __process_js_element(self, element):
        if type(element) is list:
            element = self.__process_js_element_list(element)[0]
        else:
            element = self.__process_single_js_element(element)
        return element

    def __process_js_multielement(self, elements):
        if type(elements) is list:
            elements = self.__process_js_element_list(elements)
        else:
            elements = [self.__process_single_js_element(elements)]
        return elements

    def find_element_with_js(self, js):
        element = self.execute_javascript(js)
        element = self.__process_js_element(element)
        return 1, self.__create_gui_element_dispatcher(element)

    def find_multielement(self, with_type, with_value):
        web_elements = ElementFinder.find_elements(self.__driver, with_type, with_value)
        melement = MultiElement([SeleniumDriverElementDispatcher(self, web_element) for web_element in web_elements])
        return melement.get_instance_count(), melement

    def find_multielement_with_js(self, js):
        web_elements = self.execute_javascript(js)
        web_elements = self.__process_js_multielement(web_elements)
        melement = MultiElement([SeleniumDriverElementDispatcher(self, web_element) for web_element in web_elements])
        return melement.get_instance_count(), melement

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

    def focus_on_frame(self, element_dispatcher):
        DriverCommands.focus_on_frame(self.__driver, element_dispatcher.driver_element)

    def get_element_for_setu_id(self, id):
        return self.__driver_elements[id]

    def focus_on_parent_frame(self):
        DriverCommands.focus_on_parent_frame(self.__driver)

    def focus_on_dom_root(self):
        DriverCommands.focus_on_dom_root(self.__driver)

    def perform_action_chain(self, action_chain):
        DriverCommands.perform_action_chain(self, self.__driver, action_chain)

    def hover_on_element(self, element_dispatcher):
        DriverCommands.hover_on_element(self.__driver, element_dispatcher.driver_element)



