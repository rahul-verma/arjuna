# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

import base64
import os
import time
import datetime

from arjuna.tpi.enums import ArjunaOption
from arjuna.interact.gui.auto.base.container import ElementContainer
from arjuna.interact.gui.auto.base.dispatchable import Dispatchable
from .drivercaps import DriverCapabilities
from arjuna.tpi.guiauto.source import ElementXMLSourceParser
from arjuna.interact.gui.dispatcher.selenium.driver import SeleniumDriverDispatcher
from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData
from arjuna.tpi.guiauto.element import GuiElement

class GuiAutomator(ElementContainer,Dispatchable):

    def __init__(self, app, config, ext_config=None):
        ElementContainer.__init__(self, config)
        Dispatchable.__init__(self)
        self.__app = app
        self.__econfig = ext_config
        self.__create_screenshots_dir()
        self.__main_window = None
        self.__in_slomo = config.value(ArjunaOption.GUIAUTO_SLOMO_ON)
        self.__slomo_interval = config.value(ArjunaOption.GUIAUTO_SLOMO_INTERVAL)

        from .webalert_handler import WebAlertHandler
        from .automator_conditions import GuiAutomatorConditions
        from .viewcontext_handler import ViewContextHandler
        self.__alert_handler = WebAlertHandler(self)
        self.__conditions_handler = GuiAutomatorConditions(self)
        self.__view_handler = ViewContextHandler(self)
        self.__browser = None
        self.__screenshots_dir = config.value(ArjunaOption.SCREENSHOTS_DIR)

        self.__source_parser = None

        # As of now it directly connects to Selenium Dispatcher
        # Code should be introduced here which passes through DispatcherPicker
        # based on choice of engine to support more libs.
        self.dispatcher = SeleniumDriverDispatcher()
        self.__launch()

    @property
    def app(self):
        return self.__app

    @property
    def ext_config(self):
        return self.__econfig

    @property
    def screenshots_dir(self):
        return self.__screenshots_dir

    def create_emd(self, *locators):
        return GuiElementMetaData.create_emd(*locators)

    def get_source_from_remote(self):
        return self.dispatcher.get_source()

    # def create_dispatcher(self):
    #     self._set_dispatcher(self.dispatcher_creator.create_gui_automator_dispatcher(self.config, self.setu_id))

    def slomo(self):
        if self.__in_slomo:
            time.sleep(self.__slomo_interval)

    def set_slomo(self, on, interval=None):
        self.__in_slomo = on
        if interval is not None:
            self.__slomo_interval = interval

    @property
    def browser(self):
        return self.__browser

    @property
    def main_window(self):
        return self.__main_window

    def child_window(self, emd):
        return self.get_main_window().get_child_window(emd)

    @property
    def latest_child_window(self):
        return self.get_main_window().get_latest_child_window()

    def close_all_child_windows(self):
        self.main_window.close_all_child_windows()

    def get_dom_root(self, gui):
        from arjuna.tpi.guiauto.template.frame import DomRoot
        return DomRoot(gui)

    def get_frame(self, gui, emd):
        return self.dom_root(gui).frame(emd)

    @property
    def alert_handler(self):
        return self.__alert_handler

    @property
    def view_handler(self):
        return self.__view_handler

    @property
    def conditions(self):
        return self.__conditions_handler

    def __create_screenshots_dir(self):
        sdir = self.config.value(ArjunaOption.SCREENSHOTS_DIR)
        if not os.path.isdir(sdir):
            os.makedirs(sdir)

    # #Override
    # def _get_object_uri(self):
    #     return self.__automator_uri

    def __launch(self):
        caps = DriverCapabilities(self.config, self.__econfig)
        self.dispatcher.launch(caps.processed_config)

        from arjuna.tpi.guiauto.template.window import MainWindow
        self.__main_window = MainWindow(self.app, self)

        from .browser import Browser
        self.__browser = Browser(self)

    def quit(self):
        self.dispatcher.quit()

    def __screenshot(self, file_path):
        # switch_view_context = None
        # if self.config.value(ArjunaOption.MOBILE_OS_NAME).lower() == "android":
        #     view_name = self.view_handler.get_current_view_context()   
        #     if self.view_handler._does_name_represent_web_view(view_name) :
        #         self.view_handler.switch_to_native_view() 
        #         switch_view_context = view_name

        self.dispatcher.take_screenshot(file_path)

        # if switch_view_context:
        #     self.view_handler.switch_to_view_context(switch_view_context)

    def take_screenshot(self, prefix=None):
        image_b64 = self.dispatcher.take_screenshot_as_base64()
        image = base64.b64decode(image_b64)

        ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]
        if prefix:
            prefix = prefix.replace(".py", "").replace("..", "").replace("::",".").replace(":", ".").replace("/", ".").replace("\\", ".") + "-"
        else:
            prefix = ""
        file_name = "{}{}.png".format(prefix, ts)
        fpath = os.path.join(self.screenshots_dir, file_name)
        f = open(fpath, "wb")
        f.write(image)
        f.close()
        return file_name, image_b64

    def focus_on_main_window(self):
        self.main_window.focus()

    @property
    def source(self):
        raw_source = self.get_source_from_remote()
        source_parser = ElementXMLSourceParser(raw_source, root_element="html")
        source_parser.load()
        return source_parser

    def perform_action_chain(self, single_action_chain):
        from arjuna.interact.gui.auto.automator.actions import SingleActionChain
        action_chain = SingleActionChain(self)
        action_chain.perform(single_action_chain)

    def find_element_with_js(self, js):
        return self.dispatcher.find_element_with_js(js)

    def find_multielement_with_js(self, js):
        return self.dispatcher.find_multielement_with_js(js)
    '''
        Public API
    '''

    #### Element Finding

    def element(self, gui, emd):
        from arjuna.tpi.guiauto.element import GuiElement
        gui_element = GuiElement(gui, emd) 
        self.load_element(gui_element)
        return gui_element

    def multi_element(self, gui, emd):
        from arjuna.tpi.guiauto.template.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(gui, emd)
        self.load_multielement(m_guielement)
        return m_guielement

    def dropdown(self, gui, emd):
        from arjuna.tpi.guiauto.template.dropdown import GuiWebSelect
        return GuiWebSelect(gui, emd)

    def radio_group(self, gui, emd):
        from arjuna.tpi.guiauto.template.radio_group import GuiWebRadioGroup
        return GuiWebRadioGroup(gui, emd)

    def execute_javascript(self, js, *args):
        return self.browser.execute_javascript(js, 
        *[
            isinstance(arg, GuiElement) and arg.dispatcher or arg for arg in args
        ]
        )

    ################################
    # Components
    ################################

    @property
    def alert(self):
        return self.alert_handler.create_alert()