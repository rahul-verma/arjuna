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
from arjuna.tpi.engine.asserter import AsserterMixIn
from arjuna.tpi.guiauto.model.gns import GNS
from arjuna.interact.gui.auto.finder import GuiElementFinder, GuiElementEmdFinder
from arjuna.tpi.exceptions import *

class GuiElement(AsserterMixIn, ElementContainer, Locatable, Interactable):

    def __init__(self, gui, emd):
        AsserterMixIn.__init__(self)
        ElementContainer.__init__(self, gui.automator.config)
        Locatable.__init__(self, gui, emd) #, parent, obj_name="GuiElement")
        Interactable.__init__(self, gui, emd)
        self.__gns = GNS(self, gui.gui_def)
        self.__finder = GuiElementFinder(self)
        self.__emd_finder = GuiElementEmdFinder(self)

    @property
    def finder(self):
        return self.__finder

    @property
    def emd_finder(self):
        return self.__emd_finder

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

    def _wait_until_absent(self, emd):
        try:
            self.wait_until_element_absent(emd)
        except ArjunaTimeoutError:
            raise GuiElementPresentError(self.gui, emd) 

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