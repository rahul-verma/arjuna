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


from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.interactable import Interactable
from arjuna.interact.gui.auto.base.container import ElementContainer
from arjuna.tpi.engine.asserter import _AsserterMixIn
from arjuna.tpi.guiauto.model.gns import GNS
from arjuna.interact.gui.auto.finder import GuiElementFinder, GuiElementEmdFinder
from arjuna.tpi.exceptions import *
from arjuna.core.exceptions import *
from arjuna.tpi.tracker import track

@track("info")
class GuiElement(_AsserterMixIn, ElementContainer, Locatable, Interactable):

    def __init__(self, gui, wmd):
        _AsserterMixIn.__init__(self)
        ElementContainer.__init__(self, gui._automator.config)
        Locatable.__init__(self, gui, wmd) #, parent, obj_name="GuiElement")
        Interactable.__init__(self, gui, wmd)
        self.__gns = GNS(self, gui._gui_def)
        self.__finder = GuiElementFinder(self)
        self.__wmd_finder = GuiElementEmdFinder(self)

    @property
    def _finder(self):
        return self.__finder

    @property
    def _wmd_finder(self):
        return self.__wmd_finder

    @property
    def gns(self):
        return self.__gns

    @property
    def root_element(self):
        return None

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def _wait_until_absent(self, wmd):
        try:
            self.wait_until_element_absent(wmd)
        except ArjunaTimeoutError:
            raise GuiWidgetPresentError(self.gui, wmd) 

    def wait_until_absent(self, *, fargs=None, **kwargs):
        from arjuna.tpi.guiauto.locator import GuiWidgetLocator
        wmd = GuiWidgetLocator(fmt_args=fargs, **kwargs)._as_wmd()
        self._wait_until_absent(wmd)

    def contains(self, *, fargs=None, **kwargs):
        try:
            self.element(fargs=fargs, **kwargs)
        except GuiWidgetNotPresentError:
            return False
        else:
            return True

    ########## Served by Template ########

    def locate(self, locator):
        return self._finder.locate(locator)

    def element(self, *, fargs=None, **kwargs):
        return self._finder.element(fargs=fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs):
        return self._finder.multi_element(fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs):
        return self._finder.dropdown(fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs):
        return self._finder.radio_group(fargs=fargs, **kwargs)