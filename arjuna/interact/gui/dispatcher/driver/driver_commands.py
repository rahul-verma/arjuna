# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium.webdriver.common.action_chains import ActionChains

class DriverCommands:

    @classmethod
    def go_to_url(cls, driver, url):
        driver.get(url)

    @classmethod
    def refresh_browser(cls, driver):
        driver.refresh()

    @classmethod
    def go_back_in_browser(cls, driver):
        driver.back()

    @classmethod
    def go_forward_in_browser(cls, driver):
        driver.forward()

    @classmethod
    def quit(cls, driver):
        driver.quit()

    @classmethod
    def get_page_title(cls, driver):
        return driver.title

    @classmethod
    def get_url(cls, driver):
        return driver

    @classmethod
    def get_source(cls, driver):
        return driver.page_source

    @classmethod
    def send_keys(cls, driver, key_str):
        ActionChains(driver).send_keys(key_str).perform()

    @classmethod
    def is_web_alert_present(cls, driver):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        try:
            WebDriverWait(driver, 1).until(EC.alert_is_present(),'Timed out.')
            return True
        except Exception as e:
            return False

    @classmethod
    def confirm_web_alert(cls, driver):
        driver.switch_to.alert.accept()

    @classmethod
    def dismiss_web_alert(cls, driver):
        driver.switch_to.alert.dismiss()

    @classmethod
    def send_text_to_web_alert(cls, driver, text):
        driver.switch_to.alert.send_keys(text)

    @classmethod
    def get_text_from_web_alert(cls, driver):
        return driver.switch_to.alert.text

    @classmethod
    def focus_on_frame(cls, driver, element):
        driver.switch_to.frame(element)

    @classmethod
    def focus_on_dom_root(cls, driver):
        return driver.switch_to.default_content()

    @classmethod
    def focus_on_parent_frame(cls, driver):
        driver.switch_to.parent_frame()

    @classmethod
    def execute_javascript(cls, driver, script, *args):
        from arjuna import log_debug
        log_debug("Executing JavaScript {} with args {}.".format(script, args))
        return driver.execute_script(script, *args)

    @classmethod
    def take_screenshot(cls, driver, file_path):
        return driver.save_screenshot(file_path)

    @classmethod
    def take_screenshot_as_base64(cls, driver):
        return driver.get_screenshot_as_base64()

    @classmethod
    def set_window_size(cls, driver, width, height):
        driver.set_window_size(width, height)

    @classmethod
    def maximize_window(cls, driver):
        driver.maximize_window()

    @classmethod
    def get_current_window_handle(cls, driver):
        return driver.current_window_handle

    @classmethod
    def focus_on_window(cls, driver, window_handle):
        driver.switch_to.window(window_handle)

    @classmethod
    def close_current_window(cls, driver):
        driver.close()

    @classmethod
    def get_window_title(cls, driver):
        return driver.title

    @classmethod
    def get_current_window_size(cls, driver):
        return driver.get_window_size()

    @classmethod
    def get_all_winodw_handles(cls, driver):
        return driver.window_handles

    @classmethod
    def replace_with_element(cls, setu_driver, value_tuple):
        if value_tuple[1] == True:
            return setu_driver.get_element_for_setu_id(value_tuple[0])
        else:
            return value_tuple[0]
        
    @classmethod
    def perform_action_chain(cls, setu_driver, driver, action_chain):
        chain = ActionChains(driver)
        for action in action_chain:
            kwargs = {k:cls.replace_with_element(setu_driver, v) for k,v in action[1].items()}
            getattr(chain, action[0])(**kwargs)
        chain.perform()

    @classmethod
    def hover_on_element(cls, driver, webelement):
        chain = ActionChains(driver).move_to_element(webelement).perform()

    @classmethod
    def mouse_click_on_element(cls, driver, webelement):
        chain = ActionChains(driver).click(webelement).perform()

    @classmethod
    def double_click_on_element(cls, driver, webelement):
        chain = ActionChains(driver).double_click(webelement).perform()

    @classmethod
    def scroll_to_element(cls, driver, webelement):
        cls.execute_javascript(driver, "arguments[0].scrollIntoView(true);", webelement)
