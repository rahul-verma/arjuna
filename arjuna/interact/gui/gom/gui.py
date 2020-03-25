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
import functools

from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData
from arjuna.interact.gui.helpers import Dictable

from .guidef import *
from .formatter import WithFormatter
from arjuna.engine.asserter import AsserterMixIn

from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *
from arjuna.core.exceptions import *
from arjuna.interact.gui.gom.gns import GNS

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
        
    def _load_gns(self):
        self.__gns = GNS(self, self.gui_def)

    @property
    def gns(self):
        return self.__gns

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

    def convert_to_lmd(self, meta=None, **kwargs):
        from arjuna import Arjuna
        from arjuna.interact.gui.auto.finder._with import With
        from arjuna.interact.gui.auto.finder.enums import WithType
        with_list = []
        for k,v in kwargs.items():
            if k.upper() in WithType.__members__:
                if isinstance(v, Dictable):
                    v = v.as_dict()
                with_list.append(getattr(With, k.lower())(v))
            elif Arjuna.get_withx_ref().has_locator(k):
                if isinstance(v, Dictable):
                    v = v.as_dict()
                    with_list.append(getattr(With, k.lower())(**v))
                else:
                    with_list.append(getattr(With, k.lower())(v))
        if not with_list:
            raise Exception("You must provide atleast one locator.")
        from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData
        return GuiElementMetaData.create_lmd(*with_list, meta=meta)

    @property
    def root_element(self):
        return None

    @property
    def browser(self):
        return self.automator.browser

    def format(self, **kwargs):
        return WithFormatter(self, **kwargs)

    def convert_locator_to_emd(self, locator):
        largs = locator.named_args
        if largs is None:
            largs = dict()
        emd = self.convert_to_lmd({"template": locator.template}, **largs)
        fargs = locator.fmt_args
        if fargs is None:
            fargs = dict()
        fmt_emd = emd.create_formatted_emd(**fargs)
        return fmt_emd 

    def locate(self, locator):
        from arjuna import log_debug
        emd = self.convert_locator_to_emd(locator)
        log_debug("Finding element with emd: {}.".format(emd))
        try:
            return getattr(self, "_" +  emd.meta.template.name.lower())(emd)
        except ArjunaTimeoutError:
            raise GuiElementNotPresentError(self, emd) 

    def locate_element(self, *, template="element", fargs=None, **kwargs):
        from arjuna.interact.gui.helpers import Locator
        return self.locate(Locator(template=template, fmt_args=fargs, **kwargs))

    element = locate_element

    def multi_element(self, fargs=None, **kwargs):
        return self.locate_element(template="multi_element", fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs):
        return self.locate_element(template="dropdown", fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs):
        return self.locate_element(template="radio_group", fargs=fargs, **kwargs)

    def _element(self, lmd, iconfig=None):
        return self.automator._element(self, lmd, iconfig=iconfig)

    def _multi_element(self, lmd, iconfig=None):
        return self.automator._multi_element(self, lmd, iconfig=iconfig)

    def _dropdown(self, lmd, option_container_locator=None, option_locator=None, iconfig=None):
        return self.automator._dropdown(
            self, 
            lmd,
            option_container_lmd=option_container_locator and self.convert_to_with_lmd(option_container_locator) or None,
            option_lmd=option_locator and self.convert_to_with_lmd(option_locator) or None,
            iconfig=iconfig
        )

    def _radio_group(self, lmd, iconfig=None):
        return self.automator._radio_group(self, lmd, iconfig=iconfig)

    def _wait_until_absent(self, emd):
        try:
            self.automator.wait_until_element_absent(emd)
        except ArjunaTimeoutError:
            raise GuiElementPresentError(self, emd)         

    def wait_until_absent(self, *, fargs=None, **kwargs):
        from arjuna.interact.gui.helpers import Locator
        emd = self.convert_locator_to_emd(Locator(fmt_args=fargs, **kwargs))
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


