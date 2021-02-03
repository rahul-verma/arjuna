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
from arjuna.tpi.tracker import track

class _GuiConditions:

    def __init__(self, gui):
        self.__gui = gui

    def GuiReady(self):
        caller = DynamicCaller(self.__gui.validate_readiness)
        return CommandCondition(caller)

@track("debug")
class Gui(AsserterMixIn):
    '''
        Represents a GUI.

        This is the base class for **GuiApp**, **GuiPage**, **GuiSection** and **GuiDialog**

        Keyword Arguments:
            config: Configuration object.
            ext_config: (Not Supported Yet) AutomatorExtendedConfig object for underlying GUI automator.
            label: Label for the GuiApp. If not provided, the class name is used as the label.
            gns_dir: Relative Root Directory for GNS file(s) associated with the GuiApp. Default is **<ProjectRootDirectory>/guiauto/namespace**. If provided, it is considered relative to the namespace directory.
    '''

    def __init__(self, *, gns_dir: str=None, config: 'Configuration'=None, ext_config: 'AutomatorExtendedConfig'=None, label: str=None):
        super().__init__()
        from arjuna import Arjuna
        self.__config = config is not None and config or Arjuna.get_config()
        from arjuna.tpi.constant import ArjunaOption
        ns_root_dir = self.config.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)
        self.__gns_dir = os.path.join(ns_root_dir, gns_dir)
        self.__econfig = ext_config
        self.__conditions = _GuiConditions(self)
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
        '''
            GNS Root Directory.
        '''
        return self.__gns_dir

    @property
    def _conditions(self):
        return self.__conditions

    @property
    def config(self):
        '''
            Configuration associated with this GUI.
        '''
        return self.__config

    @property
    def ext_config(self):
        '''
            AutomatorExtendedConfig associated with this GUI.
        '''
        return self.__econfig

    @property
    def label(self):
        '''
            Label for this GUI.
        '''
        return self.__label

    @property
    def name(self):
        '''
            Class Name of this GUI.
        '''
        return self.__class__.__name__

    @property
    def qual_name(self):
        '''
            Qualified Name of this GUI.
        '''
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
            self._load_anchor_element()
        except Exception as e:
            import traceback
            raise GuiNotLoadedError(self, "Anchor Element not Loaded." + str(e) + "\n" + traceback.format_exc())

        try:
            self.validate_readiness()
        except WaitableError:
            try:
                self.reach_until()
                self._conditions.GuiReady().wait(max_wait=self.config.guiauto_max_wait)
            except Exception as e:
                import traceback
                raise GuiNotLoadedError(self, str(e) + "\n" + traceback.format_exc())

    def prepare(self, *args, **kwargs):
        '''
            Part of Arjuna's GUI Loading Protocol.

            Children can override and write any necessary preparation instructions for GUI.
        '''
        pass

    def reach_until(self):
        '''
            Part of Arjuna's GUI Loading Protocol.

            Children can override and write any necessary loading instructions for GUI.
        '''
        pass

    def validate_readiness(self):
        '''
            Part of Arjuna's GUI Loading Protocol.

            Children can override and write any necessary instructions for validating readiness of the GUI.
        '''

    def _load_root_element(self):
        pass

    def _load_anchor_element(self):
        pass