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

import abc
import os
from enum import Enum
import functools

from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
from arjuna.tpi.helper.arjtype import Dictable

from arjuna.interact.gui.gom.guidef import *
from arjuna.tpi.guiauto.meta.formatter import GuiWidgetDefinitionFormatter
from arjuna.tpi.engine.asserter import AsserterMixIn

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.tpi.error import *
from arjuna.core.error import *
from arjuna.tpi.guiauto.model.gns import GNS
from arjuna.interact.gui.auto.finder import GuiFinder, GuiEmdFinder

from .gui import Gui
from arjuna.tpi.helper.image import Image
from arjuna.tpi.protocol.screen_shooter import ScreenShooter
from arjuna.tpi.tracker import track

@track("debug")
class GuiAppContent(Gui, ScreenShooter):
    '''
        Represents content of any type in a **GuiApp**.

        This is the base class for **GuiPage**, **GuiSection** and **GuiDialog** and wraps the underlying **GuiAutomator** object.

        Args:
            *args: Any number of positional argumnts. These are passed to the **prepare()** method if defined in inherited class.

        Keyword Arguments:
            automator: (Mandatory) GuiAutomator object as created by the **GuiApp**.
            label: Label for the this **GuiAppContent**. If not provided, the class name is used as the label.
            gns_dir: Relative Root Directory for GNS file(s) associated with this **GuiAppContent**. Default is the GNS directory of parent **GuiApp**.
            gns_file_name: Name of GNS file associated with this **GuiAppContent**. If not provided, default is **<label>.yaml**.
            **kwargs: Arbitrary keyword arugments. These are passed to the **prepare()** method if defined in inherited class.
    '''

    def __init__(self, *args, automator: 'GuiAutomator', label: str=None, gns_dir: str=None, gns_file_name: str=None, **kwargs):
        self.__app = automator.app
        self.__automator = automator
        gns_dir = gns_dir and gns_dir or self.app.gns_dir
        super().__init__(gns_dir=gns_dir, config=automator.config, ext_config=automator.ext_config, label=label)
        gns_file_name = gns_file_name is not None and gns_file_name or "{}.yaml".format(self.label)
        self.__def_file_path = os.path.join(self.gns_dir, gns_file_name)

        from arjuna import Arjuna
        self.__guimgr = Arjuna.get_gui_mgr()
        self.__guidef = None
        self.__gui_registered = False
        self._externalize()
        self.__gns = None

        self.__finder = GuiFinder(self)
        self.__wmd_finder = GuiEmdFinder(self)
        
    def _load_gns(self):
        self.__gns = GNS(self, self._gui_def)

    @property
    def network_recorder(self):
        return self.__automator.network_recorder

    def send_keys(self, key_chord):
        from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition
        locator = GuiWidgetDefinition(tags="body")
        body = self.locate(locator)
        body.send_keys(key_chord)

    @property
    def gns(self):
        '''
            GNS object associated with this **GuiAppContent** object.

            Encapsulates the externlized namespace and all GuiWidget meta data inside it.
        '''
        return self.__gns

    @property
    def _finder(self):
        return self.__finder

    @property
    def _wmd_finder(self):
        return self.__wmd_finder

    @property
    def app(self):
        '''
            **GuiApp** associated with this **GuiAppContent**.
        '''
        return self.__app

    @property
    def _automator(self):
        return self.__automator

    @property
    def _gui_def(self):
        return self.__guidef

    def _externalize(self):
        try:
            self.__guidef = GuiDef(self.__guimgr.name_store, self._automator, self.label, self.def_file_path)
        except Exception as e:
            import traceback
            raise GuiNamespaceLoadingError(self, str(e) + traceback.format_exc())

        from arjuna import log_debug
        log_debug("Gui Namespace loading completed for {}.".format(self.label))

    @property
    def def_file_path(self):
        '''
            Absolute GNS File path associated with this **GuiAppContent**.
        '''
        return self.__def_file_path

    def _transit(self, page):
        pass

    @property
    def _root_element(self):
        return None

    @property
    def browser(self):
        '''
            **Browser** object in which this **GuiAppContent** exists.
        '''
        return self._automator.browser

    def formatter(self, **fargs) -> GuiWidgetDefinitionFormatter:
        '''
            Create a :class:`~arjuna.tpi.guiauto.meta.formatter.GuiWidgetDefinitionFormatter` object.

            Keyword Arguments:
                **fargs: Arbitrary key-value pairs to be used for formatting identifiers in `GuiWidgetDefinition`.
        '''
        return GuiWidgetDefinitionFormatter(self, **fargs)

    def _wait_until_absent(self, wmd):
        try:
            self._automator._wait_until_element_absent(wmd)
        except ArjunaTimeoutError:
            raise GuiWidgetPresentError(self, wmd)         

    def wait_until_absent(self, *, fargs=None, **kwargs):
        '''
            Wait until a **GuiWidget** is absent.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(**kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Note:
                By default Wait is done until **ArjunaOption.GUIAUTO_MAX_WAIT** in the **Configuration** object associated with this **GuiAppContent**.

                You can pass **max_wait** argument to change this. Value is considered in seconds.
        '''
        from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition
        wmd = GuiWidgetDefinition(fmt_args=fargs, **kwargs)._as_wmd()
        self._wait_until_absent(wmd)

    def contains(self, *, fargs=None, **kwargs):
        '''
            Check whether this **GuiAppContent** object contains a **GuiWidget**. Includes dynamic waiting.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(**kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Note:
                By default Wait is done until **ArjunaOption.GUIAUTO_MAX_WAIT** in the **Configuration** object associated with this **GuiAppContent**.

                You can pass **max_wait** argument to change this. Value is considered in seconds.
        '''
        try:
            self.element(fargs=fargs, **kwargs)
        except GuiWidgetNotPresentError:
            return False
        else:
            return True

    @property
    def _dom_root(self):
        '''
            **GuiApp** associated with this **GuiAppContent**.
        '''
        return self._automator.dom_root(self)

    def _frame(self, *str_or_with_locators):
        return self._automator.frame(self, self.convert_to_with_wmd(*str_or_with_locators))

    @property
    def _alert(self):
        return self._automator.alert

    @property
    def title(self):
        '''
            (Not Supported Yet) Title of the window containing this **GuiAppContent**.
        '''
        return self.app.main_window.title

    def set_slomo(self, *, on, interval=None):
        '''
            (Not Supported Yet) Set Slow Motion mode.

            Keyword Arguments:
                on: If True the mode is switched on.
                interval: Number of seconds between successive actions.
        '''
        self._automator.set_slomo(on, interval)

    def execute_javascript(self, js, *args):
        '''
            Inject and Execute JavaScript.

            Args:
                js: Arbitrary JavaScript
                *args: Any number of positional arguments used for formatting of JavaScript by underlying automation engine.
        '''
        return self._automator.execute_javascript(js, *args)

    def _take_screenshot(self, prefix: str=None) -> Image:
        return self._automator.take_screenshot(prefix=prefix)

    def go_to_url(self, url: str=None):
        '''
            Go to a URL. 

            This action takes place in the current browser window/tab.
        '''
        self.browser.go_to_url(url)

    def _load_anchor_element(self):
        label = self._gui_def.anchor_element_name

        from arjuna import log_debug
        log_debug("Loading Anchor Element for {} Gui. anchor label in GNS: {}.".format(
            self.label,
            self._gui_def.anchor_element_name,
        ))

        if label is not None:
            getattr(self.gns, label)

    def locate(self, locator) -> 'GuiWidget':
        '''
           Locate a `GuiWidget`.

           Arguments:
            locator: `GuiWidgetDefinition` object.

            Returns:
                An object of type `GuiWidget`. Exact object type depends on the value of **type** attribute in `GuiWidgetDefinition`. 
        '''
        return self._finder.locate(locator)

    def element(self, *, fargs=None, **kwargs):
        '''
            Locate a `GuiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiElement` object.
        '''
        return self._finder.element(fargs=fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs):
        '''
            Locate a `GuiMultiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiMultiElement` object.
        '''
        return self._finder.multi_element(fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs):
        '''
            Locate a `GuiDropDown`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiDropDown` object.
        '''
        return self._finder.dropdown(fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs):
        '''
            Locate a `GuiRadioGroup`

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiRadioGroup` object
        '''
        return self._finder.radio_group(fargs=fargs, **kwargs)


