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
        from arjuna.core.enums import ArjunaOption
        ns_root_dir = self.get_config().value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)
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

    def get_gns_dir(self):
        return self.__gns_dir

    def get_conditions(self):
        return self.__conditions

    def get_config(self):
        return self.__config

    def get_ext_config(self):
        return self.__econfig

    def get_label(self):
        return self.__label

    def get_name(self):
        return self.__class__.__name__

    def get_qual_name(self):
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
                self.conditions.GuiReady().wait(max_wait_time=self.get_config().guiauto_max_wait)
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

class AppContent(Gui):

    def __init__(self, *args, automator, label=None, gns_dir=None, gns_file_name=None, **kwargs):
        self.__app = automator.get_app()
        self.__automator = automator
        gns_dir = gns_dir and gns_dir or self.get_app().get_gns_dir()
        super().__init__(gns_dir=gns_dir, config=automator.get_config(), ext_config=automator.get_ext_config(), label=label)
        gns_file_name = gns_file_name is not None and gns_file_name or "{}.yaml".format(self.get_label())
        self.__def_file_path = os.path.join(self.get_gns_dir(), gns_file_name)

        from arjuna import Arjuna
        self.__guimgr = Arjuna.get_gui_mgr()
        self.__guidef = None
        self.__gui_registered = False
        self._externalize()

    def get_app(self):
        return self.__app

    def get_automator(self):
        return self.__automator

    def get_gui_def(self):
        return self.__guidef

    def _externalize(self):
        try:
            self.__guidef = GuiDef(self.__guimgr.name_store, self.get_automator(), self.get_label(), self.get_def_file_path())
        except Exception as e:
            import traceback
            raise GuiNamespaceLoadingError(self, str(e) + traceback.format_exc())

        from arjuna import Arjuna
        Arjuna.get_logger().debug("Gui Namespace loading completed for {}.".format(self.get_label()))

    def get_def_file_path(self):
        return self.__def_file_path

    def transit(self, page):
        pass

    # def convert_to_with_lmd(self, *raw_str_or_with_locators, nested_element=False):
    #     from arjuna.interact.gui.helpers import With, WithType
    #     out = []
    #     for locator in raw_str_or_with_locators:
    #         w = None
    #         if isinstance(locator, With):
    #             w = locator
    #         elif type(locator) is str:
    #             w = With.label(locator)
    #         elif isinstance(locator, Enum):
    #             w = With.label(locator.name)
    #         else:
    #             raise Exception("A With object or name of element is expected as argument.")

    #         if w.wtype == WithType.LABEL:
    #             if isinstance(w.wvalue, Enum):
    #                 w.wvalue = w.wvalue.name
    #             out.extend(self.gui_def.convert_to_with(w))
    #         else:
    #             out.append(w)
    #     lmd = GuiElementMetaData.create_lmd(*out)
    #     return lmd

    def get_browser(self):
        return self.get_automator().get_browser()

    def __element(self, *str_or_with_locators, iconfig=None):
        return self.get_automator().element(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def __multi_element(self, *str_or_with_locators, iconfig=None):
        return self.get_automator().multi_element(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def __dropdown(self, *str_or_with_locators, option_container_locator=None, option_locator=None, iconfig=None):
        return self.get_automator().dropdown(
            self, 
            self.convert_to_with_lmd(*str_or_with_locators),
            option_container_lmd=option_container_locator and self.convert_to_with_lmd(option_container_locator) or None,
            option_lmd=option_locator and self.convert_to_with_lmd(option_locator) or None,
            iconfig=iconfig
        )

    def __radio_group(self, *str_or_with_locators, iconfig=None):
        return self.get_automator().radio_group(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def __tab_group(self, *str_or_with_locators, tab_header_locator, content_relation_attr, content_relation_type, iconfig=None):
        return self.get_automator().tab_group(
            self,
            self.convert_to_with_lmd(*str_or_with_locators),
            tab_header_lmd=self.convert_to_with_lmd(tab_header_locator),
            content_relation_attr=content_relation_attr, 
            content_relation_type=content_relation_type, 
            iconfig=iconfig
        )

    def wait_until_element_absent(self, name):
        return self.get_automator().wait_until_element_absent(self.get_gui_def().get_emd(name))

    def get_dom_root(self):
        return self.get_automator().dom_root(self)

    def frame(self, *str_or_with_locators, iconfig=None):
        return self.get_automator().frame(self, self.convert_to_with_lmd(*str_or_with_locators), iconfig=iconfig)

    def get_alert(self):
        return self.get_automator().alert

    def get_title(self):
        return self.get_main_window().get_title()

    def get_main_window(self):
        return self.get_automator().get_main_window()

    def get_child_window(self, *str_or_with_locators):
        return self.get_automator().child_window(self.convert_to_with_lmd(*str_or_with_locators))

    def get_latest_child_window(self):
        return self.get_automator().latest_child_window

    def close_all_child_windows(self):
        self.get_automator().close_all_child_windows()

    def set_slomo(self, on, interval=None):
        self.get_automator().set_slomo(on, interval)

    def execute_javascript(self, js, *args):
        return self.get_automator().execute_javascript(js, *args)

    def take_screenshot(self, prefix=None):
        return self.get_automator().take_screenshot(prefix=prefix)

    def go_to_url(self, url):
        self.get_browser().go_to_url(url)

    def load_anchor_element(self):
        label = self.get_gui_def().anchor_element_name

        from arjuna import Arjuna
        Arjuna.get_logger().debug("Loading Anchor Element for {} Gui. anchor label in GNS: {}.".format(
            self.get_label(),
            self.get_gui_def().anchor_element_name,
        ))

        if label is not None:
            getattr(self, label)

    def __getattr__(self, name):
        print(name)
        emd = self.get_gui_def().get_emd(name)
        from arjuna import Arjuna
        Arjuna.get_logger().debug("Finding element for emd: {}".format(emd))
        return getattr(self.get_automator(), emd.meta.template.name.lower())(self, emd)


