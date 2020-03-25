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

from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.interactable import Interactable
from arjuna.interact.gui.auto.base.container import ElementContainer
from arjuna.engine.asserter import AsserterMixIn
from arjuna.interact.gui.gom.gns import GNS
from arjuna.core.exceptions import *

class GuiElement(AsserterMixIn, ElementContainer, Locatable, Interactable):

    def __init__(self, gui, emd, iconfig=None):
        AsserterMixIn.__init__(self)
        ElementContainer.__init__(self, gui.automator.config)
        Locatable.__init__(self, gui, emd) #, parent, obj_name="GuiElement")
        Interactable.__init__(self, gui, iconfig)
        self.__gns = GNS(self, gui.gui_def)

    @property
    def gns(self):
        return self.__gns

    @property
    def root_element(self):
        return None

    def __element(self, *str_or_with_locators, iconfig=None):
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        return self.element(self.gui, lmd, iconfig=iconfig)

    def _element(self, gui, lmd, iconfig=None):
        from arjuna.interact.gui.auto.element.guielement import GuiElement
        gui_element = GuiElement(gui, lmd, iconfig=iconfig)
        self.load_element(gui_element)
        return gui_element        

    def __multi_element(self, *str_or_with_locators, iconfig=None):
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        return self.multi_element(self.gui, lmd, iconfig=iconfig)

    def _multi_element(self, gui, lmd, iconfig=None):
        from arjuna.interact.gui.auto.element.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(gui, lmd, iconfig=iconfig)
        self.load_multielement(m_guielement)
        return m_guielement

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def locate(self, locator):
        from arjuna import log_debug
        emd = self.gui.convert_locator_to_emd(locator)
        log_debug("Finding element with emd: {}.".format(emd))
        try:
            return getattr(self, "_" +  emd.meta.template.name.lower())(self.gui, emd)
        except ArjunaTimeoutError:
            raise GuiElementNotPresentError(self.gui, emd)        

    def locate_element(self, *, template="element", fargs=None, **kwargs):
        from arjuna.interact.gui.helpers import Locator
        return self.locate(Locator(template=template, fmt_args=fargs, **kwargs))

    element = locate_element

    def multi_element(self, **kwargs):
        return self.locate_element(template="multi_element", **kwargs)

    def _wait_until_absent(self, emd):
        try:
            self.wait_until_element_absent(emd)
        except ArjunaTimeoutError:
            raise GuiElementPresentError(self.gui, emd) 

    def wait_until_absent(self, *, fargs=None, **kwargs):
        from arjuna.interact.gui.helpers import Locator
        emd = self.gui.convert_locator_to_emd(Locator(fmt_args=fargs, **kwargs))
        self._wait_until_absent(emd)

    def contains(self, *, fargs=None, **kwargs):
        try:
            self.element(fargs=fargs, **kwargs)
        except GuiElementNotPresentError:
            return False
        else:
            return True