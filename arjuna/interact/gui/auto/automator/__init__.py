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

import base64
import os
import time
import datetime
import json

from arjuna.tpi.constant import ArjunaOption
from arjuna.tpi.guiauto.base.container import GuiWidgetContainer
from arjuna.interact.gui.auto.base.dispatchable import _Dispatchable
from .drivercaps import DriverCapabilities
from arjuna.tpi.guiauto.source.page import GuiPageSource
from arjuna.interact.gui.dispatcher.selenium.driver import SeleniumDriverDispatcher
from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
from arjuna.tpi.guiauto.widget.element import GuiElement
from arjuna.tpi.helper.image import Image
from arjuna.interact.gui.auto.automator.network_recorder import BrowserMobNetworkRecorder
from arjuna import track, log_debug

@track("debug")
class GuiAutomator(GuiWidgetContainer,_Dispatchable):

    def __init__(self, app, config, ext_config=None):
        GuiWidgetContainer.__init__(self, config)
        _Dispatchable.__init__(self)
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
        self._dispatcher = SeleniumDriverDispatcher()
        self._network_recorder = BrowserMobNetworkRecorder(self)
        self.__launch()

    @property
    def app(self):
        return self.__app

    @property
    def ext_config(self):
        return self.__econfig

    @property
    def network_recorder(self):
        return self._network_recorder

    @property
    def screenshots_dir(self):
        return self.__screenshots_dir

    def create_wmd(self, *locators):
        return GuiWidgetMetaData.create_wmd(*locators)

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

    def child_window(self, wmd):
        return self.get_main_window().get_child_window(wmd)

    @property
    def latest_child_window(self):
        return self.get_main_window().get_latest_child_window()

    def close_all_child_windows(self):
        self.main_window.close_all_child_windows()

    def get_dom_root(self, gui):
        raise NotImplementedError()
        # from arjuna.tpi.guiauto.widget.frame import DomRoot
        # return DomRoot(gui)

    def get_frame(self, gui, wmd):
        return self.dom_root(gui).frame(wmd)

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

        from arjuna.tpi.guiauto.obj.window import MainWindow
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
            import re
            prefix = re.sub(r"\[.*?\]", "", prefix)
            prefix = prefix.replace(".py", "").replace("..", "").replace("::",".").replace(":", ".").replace("/", ".").replace("\\", ".") + "-"
        else:
            prefix = ""
        file_name = "{}{}.png".format(prefix, ts)
        fpath = os.path.join(self.screenshots_dir, file_name)
        f = open(fpath, "wb")
        f.write(image)
        f.close()
        img = Image(fpath=fpath, b64=image_b64)

        from arjuna import Arjuna
        Arjuna.get_report_metadata().add_image(img)
        return img

    def focus_on_main_window(self):
        self.main_window.focus()

    @property
    def source(self) -> GuiPageSource:
        raw_source = self.get_source_from_remote()
        source_parser = GuiPageSource(raw_source)
        source_parser._load()
        return source_parser

    def perform_action_chain(self, single_action_chain):
        from arjuna.interact.gui.auto.automator.actions import SingleActionChain
        action_chain = SingleActionChain(self)
        action_chain.perform(single_action_chain)

    def _find_element_with_js(self, js):
        return self.dispatcher.find_element_with_js(js)

    def _find_multielement_with_js(self, js):
        return self.dispatcher.find_multielement_with_js(js)
    '''
        Public API
    '''

    #### Element Finding

    def element(self, gui, wmd):
        from arjuna.tpi.guiauto.widget.element import GuiElement
        gui_element = GuiElement(gui, wmd) 
        self._load_element(gui_element)
        return gui_element

    def multi_element(self, gui, wmd):
        from arjuna.tpi.guiauto.widget.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(gui, wmd)
        self._load_multielement(m_guielement)
        return m_guielement

    def dropdown(self, gui, wmd):
        from arjuna.tpi.guiauto.widget.dropdown import GuiDropDown
        return GuiDropDown(gui, wmd)

    def radio_group(self, gui, wmd):
        from arjuna.tpi.guiauto.widget.radio_group import GuiRadioGroup
        return GuiRadioGroup(gui, wmd)

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