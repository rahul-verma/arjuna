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

import traceback
from arjuna.tpi.constant import ArjunaOption
from arjuna.interact.gui.auto.finder.wmd import SimpleGuiWidgetMetaData

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.tpi.error import ChildWindowNotFoundError

class WindowConditions:

    def __init__(self, window):
        self.__window = window

    @property
    def window(self):
        return self.__window

    def ChildWindowIsPresent(self, wmd):
        caller = DynamicCaller(self.window._find_child_window, wmd)
        return CommandCondition(caller)

class BasicWindow:

    def __init__(self, app, automator):
        super().__init__()
        self.__app = app
        self.__automator = automator
        self.__window_handle = None
        self.__config = automator.config

    @property
    def max_wait(self):
        return self.__automator.config.guiauto_max_wait

    @property
    def app(self):
        return self.__app

    @property
    def config(self):
        return self.__config    

    @property
    def _automator(self):
        return self.__automator

    @property
    def handle(self):
        return self.__window_handle

    @property
    def title(self):
        return self.__automator.dispatcher.get_current_window_title()

    @property
    def size(self):
        return self.__automator.dispatcher.get_current_window_size()

    def _set_handle(self, handle):
        self.__window_handle = handle

    def focus(self):
        self.__automator.dispatcher.focus_on_window(self.handle)

    def is_main_window(self):
        return False

    def set_window_size(self, width, height):
        self.__automator.dispatcher.set_current_window_size(width, height)

    def maximize(self):
        self.__automator.dispatcher.maximize_current_window()

class MainWindow(BasicWindow):

    def __init__(self, app, automator):
        super().__init__(app, automator)
        self._set_handle(self.get_current_window_handle()) 
        self.__all_child_windows = {}
        self.__setu_id_map = {}
        self.__resize_window_as_per_config()
        self.__conditions = WindowConditions(self)

    @property
    def conditions(self):
        return self.__conditions

    def get_all_child_window_handles(self):
        handles = self.__automator.dispatcher.get_all_window_handles()
        handles = [handle for handle in handles if handle != self.handle]
        new_handles = []
        for handle in handles:
            if handle != self.handle:
                if handle not in self.__all_child_windows:
                    cwin = ChildWindow(self.app, self.__automator, self, handle)
                    self.__all_child_windows[handle] = cwin
                    new_handles.append(handle)
        return handles, new_handles

    @property
    def latest_child_window(self):
        _, new_handles = self.get_all_child_window_handles()
        if not new_handles:
            raise Exception("No new window was launched.")
        elif len(new_handles) > 1:
            raise Exception("Multiple new windows were launched, so can not deterministically jump to a new window.")
        return self.__all_child_windows[new_handles[0]]

    def __get_child_window(self, handle):
        return self.__all_child_windows[handle]

    def __focus_on_window(self, handle):
        self.__get_child_window(handle).jump()

    def delete_window(self, handle):
        del self.__all_child_windows[handle]

    def close_all_child_windows(self):
        all_child_handles, _ = self.get_all_child_window_handles()
        for handle in all_child_handles:
            cwin = self.__get_child_window(handle)
            cwin.focus()
            cwin.close()
        self.focus()

    def get_current_window_handle(self):
        return self._automator.dispatcher.get_current_window_handle()

    def child_window(self, wmd):
        return self.get_conditions().ChildWindowIsPresent(wmd).wait(max_wait=self.max_wait)

    def _find_child_window(self, wmd):
        all_child_handles, _ = self.get_all_child_window_handles()
        for handle in all_child_handles:
            cwin = self.__get_child_window(handle)
            cwin.focus()
            for locator in wmd.locators:
                if locator.ltype.name == "WINDOW_TITLE":
                    if cwin.title.lower() == locator.lvalue.lower():
                        return cwin
                elif locator.ltype.name == "WINDOW_PTITLE":
                    if locator.lvalue.lower() in cwin.title.lower():
                        return cwin
                elif locator.ltype.name == "CONTENT_LOCATOR":
                    for child_locator in locator.lvalue.locators:
                        try:
                            wmd = SimpleGuiWidgetMetaData(child_locator.ltype.name, child_locator.lvalue)
                            # The element for window is created in the context of an app.
                            # Need to verify this logic.
                            # and its impact on POM.
                            contained_element = self.__automator.element(self.app,wmd, max_wait=0.5)
                            # contained_element.find()
                            return cwin
                        except WaitableError as f:
                            continue  
                        except Exception as e:
                            raise Exception(str(e) + traceback.format_exc())                          
        
        raise ChildWindowNotFoundError(*wmd.locators)

    def __resize_window_as_per_config(self):
        # Resize window
        config = self.config
        browser_width = config.value(ArjunaOption.BROWSER_DIM_WIDTH)
        browser_height = config.value(ArjunaOption.BROWSER_DIM_HEIGHT)
        should_maximize = config.value(ArjunaOption.BROWSER_MAXIMIZE)

        if config.is_arjuna_option_not_set(ArjunaOption.BROWSER_DIM_WIDTH) and config.is_arjuna_option_not_set(ArjunaOption.BROWSER_DIM_HEIGHT):
            if should_maximize:
                self.maximize()
        else:
            width, height = None, None
            current_width, current_height = self.get_size()
            width = config.is_arjuna_option_not_set(ArjunaOption.BROWSER_DIM_WIDTH) and browser_width or current_width
            height = config.is_arjuna_option_not_set(ArjunaOption.BROWSER_DIM_HEIGHT) and browser_height or current_height
            self.set_window_size(width, height)

    def is_main_window(self):
        return True

    def close(self):
        raise Exception("You can not close main window. Use automator.quit() to quit application.")

class ChildWindow(BasicWindow):

    def __init__(self, app, automator, main_window, handle):
        super().__init__(app, automator)
        self.__main_window = main_window
        self._set_handle(handle) 

    def close(self):
        self.focus()
        self._automator.dispatcher.close_current_window()
        self.__main_window.delete_window(self.handle)
        self.__main_window.focus()