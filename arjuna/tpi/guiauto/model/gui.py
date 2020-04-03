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

import abc
import os
from enum import Enum
import functools

from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData
from arjuna.tpi.guiauto.helpers import Dictable

from arjuna.interact.gui.gom.guidef import *
from .formatter import WithFormatter
from arjuna.tpi.engine.asserter import AsserterMixIn

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.tpi.exceptions import *
from arjuna.tpi.guiauto.model.gns import GNS
from arjuna.interact.gui.auto.finder import GuiFinder, GuiEmdFinder

class GuiConditions:

    def __init__(self, gui):
        self.__gui = gui

    def GuiReady(self):
        caller = DynamicCaller(self.__gui.validate_readiness)
        return CommandCondition(caller)

class Gui(AsserterMixIn):

    def __init__(self, *, gns_dir, config=None, ext_config=None, label=None):
        '''
            You can either provide automator.
        '''
        super().__init__()
        from arjuna import Arjuna
        self.__config = config is not None and config or Arjuna.get_config()
        from arjuna.tpi.enums import ArjunaOption
        ns_root_dir = self.config.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)
        self.__gns_dir = os.path.join(ns_root_dir, gns_dir)
        self.__econfig = ext_config
        self.__conditions = GuiConditions(self)
        if ext_config is None:
            self.__econfig = dict()
        else:
            if type(ext_config) is dict:
                self.__econfig = ext_config
            else:
                self.__econfig = ext_config.config
        self.__label = label is not None and label or self.__class__.__name__

    @property
    def gns_dir(self):
        return self.__gns_dir

    @property
    def conditions(self):
        return self.__conditions

    @property
    def config(self):
        return self.__config

    @property
    def ext_config(self):
        return self.__econfig

    @property
    def label(self):
        return self.__label

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def qual_name(self):
        return self.__class__.__qualname__

    def _load(self, *args, **kwargs):
        self.prepare(*args, **kwargs)
        try:
            self._load_root_element()
        except Exception as e:
            import traceback
            raise GuiNotLoadedError(self, "Root Element not Loaded. " + str(e) + "\n" + traceback.format_exc())

        self._load_gns()

        try:
            self.load_anchor_element()
        except Exception as e:
            import traceback
            raise GuiNotLoadedError(self, "Anchor Element not Loaded." + str(e) + "\n" + traceback.format_exc())

        try:
            self.validate_readiness()
        except WaitableError:
            try:
                self.reach_until()
                self.conditions.GuiReady().wait(max_wait=self.config.guiauto_max_wait)
            except Exception as e:
                import traceback
                raise GuiNotLoadedError(self, str(e) + "\n" + traceback.format_exc())

    def prepare(self):
        # Children can override and write any necessary preparation instructions e.g. externalizing
        pass

    def reach_until(self):
        # Children can override and write any necessary loading instructions
        pass

    def validate_readiness(self):
        pass

    def _load_root_element(self):
        pass

    def load_anchor_element(self):
        pass

class AppContent(Gui):

    def __init__(self, *args, automator, label=None, gns_dir=None, gns_file_name=None, **kwargs):
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
        self.__emd_finder = GuiEmdFinder(self)
        
    def _load_gns(self):
        self.__gns = GNS(self, self.gui_def)

    @property
    def gns(self):
        return self.__gns

    @property
    def finder(self):
        return self.__finder

    @property
    def emd_finder(self):
        return self.__emd_finder

    @property
    def app(self):
        return self.__app

    @property
    def automator(self):
        return self.__automator

    @property
    def gui_def(self):
        return self.__guidef

    def _externalize(self):
        try:
            self.__guidef = GuiDef(self.__guimgr.name_store, self.automator, self.label, self.def_file_path)
        except Exception as e:
            import traceback
            raise GuiNamespaceLoadingError(self, str(e) + traceback.format_exc())

        from arjuna import Arjuna
        Arjuna.get_logger().debug("Gui Namespace loading completed for {}.".format(self.label))

    @property
    def def_file_path(self):
        return self.__def_file_path

    def transit(self, page):
        pass

    @property
    def root_element(self):
        return None

    @property
    def browser(self):
        return self.automator.browser

    def format(self, **kwargs):
        return WithFormatter(self, **kwargs)

    def _wait_until_absent(self, emd):
        try:
            self.automator.wait_until_element_absent(emd)
        except ArjunaTimeoutError:
            raise GuiElementPresentError(self, emd)         

    def wait_until_absent(self, *, fargs=None, **kwargs):
        from arjuna.tpi.guiauto.helpers import Locator
        emd = Locator(fmt_args=fargs, **kwargs).as_emd()
        self._wait_until_absent(emd)

    def contains(self, *, fargs=None, **kwargs):
        try:
            self.element(fargs=fargs, **kwargs)
        except GuiElementNotPresentError:
            return False
        else:
            return True

    @property
    def dom_root(self):
        return self.automator.dom_root(self)

    def frame(self, *str_or_with_locators):
        return self.automator.frame(self, self.convert_to_with_emd(*str_or_with_locators))

    @property
    def alert(self):
        return self.automator.alert

    @property
    def title(self):
        return self.main_window.title

    @property
    def main_window(self):
        return self.automator.main_window

    def child_window(self, *str_or_with_locators):
        return self.automator.child_window(self.convert_to_with_emd(*str_or_with_locators))

    @property
    def latest_child_window(self):
        return self.automator.latest_child_window

    def close_all_child_windows(self):
        self.automator.close_all_child_windows()

    def set_slomo(self, on, interval=None):
        self.automator.set_slomo(on, interval)

    def execute_javascript(self, js, *args):
        return self.automator.execute_javascript(js, *args)

    def take_screenshot(self, prefix=None):
        return self.automator.take_screenshot(prefix=prefix)

    def go_to_url(self, url):
        self.browser.go_to_url(url)

    def load_anchor_element(self):
        label = self.gui_def.anchor_element_name

        from arjuna import Arjuna
        Arjuna.get_logger().debug("Loading Anchor Element for {} Gui. anchor label in GNS: {}.".format(
            self.label,
            self.gui_def.anchor_element_name,
        ))

        if label is not None:
            getattr(self.gns, label)

    @property
    def source(self):
        return self.automator.source


    ########## Served by Template ########

    def locate(self, locator):
        return self.finder.locate(locator)

    def element(self, *, fargs=None, **kwargs):
        return self.finder.element(fargs=fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs):
        return self.finder.multi_element(fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs):
        return self.finder.dropdown(fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs):
        return self.finder.radio_group(fargs=fargs, **kwargs)


