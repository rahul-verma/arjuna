'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


import abc
import os
from enum import Enum
import unittest

from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData

from .guidef import *
from arjuna.engine.asserter import AsserterMixIn

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.core.exceptions import WaitableError, GuiNotLoadedError, GuiNamespaceLoadingError

class GuiConditions:

    def __init__(self, gui):
        self.__gui = gui

    @property
    def gui(self):
        return self.__gui

    def GuiReady(self):
        caller = DynamicCaller(self.gui.validate_readiness)
        return CommandCondition(caller)

class Gui(AsserterMixIn):

    def __init__(self, *, config=None, ext_config=None, label=None):
        '''
            You can either provide automator.
        '''
        super().__init__()
        from arjuna import Arjuna
        self.__config = config is not None and config or Arjuna.get_ref_config()
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
        self.__externalized = False

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
            self.load_root_element()
        except Exception as e:
            import traceback
            raise GuiNotLoadedError(self, "Root Element not Loaded. " + str(e) + "\n" + traceback.format_exc())

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
                self.conditions.GuiReady().wait(max_wait_time=self.config.guiauto_max_wait)
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

    def load_root_element(self):
        pass

    def load_anchor_element(self):
        pass

    @property
    def externalized(self):
        return self.__externalized

    def _set_externalized(self):
        self.__externalized = True

class AppContent(Gui):

    def __init__(self, *args, automator, label=None, **kwargs):
        super().__init__(config=automator.config, ext_config=automator.ext_config, label=label)
        self.__app = automator.app
        self.__automator = automator
        from arjuna import Arjuna
        self.__guimgr = Arjuna.get_gui_mgr()
        self.__guidef = None

        self.__gui_registered = False
        self.__gns_file_name = None
        self.__def_file_path = None

    @property
    def app(self):
        return self.__app
    
    @property
    def automator(self):
        return self.__automator

    @property
    def gui_def(self):
        return self.__guidef

    def externalize(self, gns_dir=None, gns_file_name=None):
        self.__gns_file_name = gns_file_name is not None and gns_file_name or "{}.yaml".format(self.label)        
        from arjuna.core.enums import ArjunaOption
        gns_dir = gns_dir and gns_dir or self.app.gns_dir
        if not gns_dir:
            gns_dir = ""
        ns_root_dir = self.config.arjuna_options.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)
        
        self.__def_file_path = os.path.join(ns_root_dir, gns_dir, self.gns_file_name)
        try:
            self.__guidef = GuiDef(self.__guimgr.name_store, self.automator, self.label, self.__def_file_path) # self.__guimgr.namespace_dir, 
        except Exception as e:
            import traceback
            raise GuiNamespaceLoadingError(self, str(e) + traceback.format_exc())

        from arjuna import Arjuna
        Arjuna.get_logger().debug("Gui Namespace loading completed for {}.".format(self.label))
        self._set_externalized()

    @property
    def gns_file_name(self):
        return self.__gns_file_name

    @property
    def def_file_path(self):
        return self.__def_file_path

    def transit(self, page):
        pass

    def convert_to_with_lmd(self, *raw_str_or_with_locators, nested_element=False):
        from arjuna.interact.gui.helpers import With, WithType
        out = []
        for locator in raw_str_or_with_locators:
            w = None
            if isinstance(locator, With):
                w = locator
            elif type(locator) is str:
                w = With.label(locator)
            elif isinstance(locator, Enum):
                w = With.label(locator.name)
            else:
                raise Exception("A With object or name of element is expected as argument.")

            if w.wtype == WithType.LABEL:
                if isinstance(w.wvalue, Enum):
                    w.wvalue = w.wvalue.name
                out.extend(self.gui_def.convert_to_with(w))
            else:
                out.append(w)
        lmd = GuiElementMetaData.create_lmd(*out)
        return lmd

    @property
    def browser(self):
        return self.impl_gui.browser

    def element(self, *str_or_with_locators, iconfig=None):
        return self.automator.element(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def multi_element(self, *str_or_with_locators, iconfig=None):
        return self.automator.multi_element(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def dropdown(self, *str_or_with_locators, option_container_locator=None, option_locator=None, iconfig=None):
        return self.automator.dropdown(
            self, 
            self.convert_to_with_lmd(*str_or_with_locators),
            option_container_lmd=option_container_locator and self.convert_to_with_lmd(option_container_locator) or None,
            option_lmd=option_locator and self.convert_to_with_lmd(option_locator) or None,
            iconfig=iconfig
        )

    def radio_group(self, *str_or_with_locators, iconfig=None):
        return self.automator.radio_group(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def tab_group(self, *str_or_with_locators, tab_header_locator, content_relation_attr, content_relation_type, iconfig=None):
        return self.automator.tab_group(
            self,
            self.convert_to_with_lmd(*str_or_with_locators),
            tab_header_lmd=self.convert_to_with_lmd(tab_header_locator),
            content_relation_attr=content_relation_attr, 
            content_relation_type=content_relation_type, 
            iconfig=iconfig
        )

    def wait_until_element_absent(self, *str_or_with_locators):
        return self.automator.wait_until_element_absent(self.convert_to_with_lmd(*str_or_with_locators))

    @property
    def dom_root(self):
        return self.automator.dom_root(self)

    def frame(self, *str_or_with_locators, iconfig=None):
        return self.automator.frame(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

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
        return self.automator.child_window(self.convert_to_with_lmd(*str_or_with_locators))

    @property
    def latest_child_window(self):
        return self.automator.latest_child_window

    def close_all_child_windows(self):
        self.automator.close_all_child_windows()

    @property
    def browser(self):
        return self.automator.browser

    def set_slomo(self, on, interval=None):
        self.automator.set_slomo(on, interval)

    def execute_javascript(self, js, *args):
        return self.automator.execute_javascript(js, *args)

    def take_screenshot(self, prefix=None):
        return self.automator.take_screenshot(prefix=prefix)

    def go_to_url(self, url):
        self.browser.go_to_url(url)

    def load_anchor_element(self):
        if self.externalized:
            locators = self.gui_def.anchor_element_with_locators

            from arjuna import Arjuna
            Arjuna.get_logger().debug("Loading State Element for {} widget. __state__ locators in GNS: {}.".format(
                self.label,
                GuiElementMetaData.locators_as_str(locators),
            ))

            if locators is not None:
                self.element(*locators)


