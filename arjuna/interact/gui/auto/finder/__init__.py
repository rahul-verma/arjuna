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

from functools import partial
from arjuna.tpi.exceptions import *
from arjuna.tpi.guiauto.helpers import Locator

class GuiEmdFinder:

    def __init__(self, gui):
        self.__gui = gui
        self.__automator = gui.automator

    def __getattr__(self, name):
        return partial(getattr(self.__automator, name.lower()), self.__gui)

class GuiFinder:

    def __init__(self, gui):
        self.__emd_finder = GuiEmdFinder(gui)
        self.__gui = gui

    def locate(self, locator):
        from arjuna import log_debug
        from arjuna.tpi.exceptions import ArjunaTimeoutError, GuiElementNotPresentError
        emd = locator.as_emd()
        log_debug("Finding element with emd: {}.".format(emd))
        try:
            return getattr(self.__emd_finder, emd.meta["template"].name.lower())(emd)
        except ArjunaTimeoutError:
            raise GuiElementNotPresentError(self.__gui, emd)         

    def __locate_interim(self, name):
        def finder(fargs=None, **kwargs):
            locator = Locator(template=name, fmt_args=fargs, **kwargs)
            return self.locate(locator)
        return finder

    def __getattr__(self, name):
        return self.__locate_interim(name)

class GuiElementEmdFinder:

    def __init__(self, gui_element):
        self.__gui_element = gui_element

    def element(self, emd):
        from arjuna.tpi.guiauto.element import GuiElement
        gui_element = GuiElement(self.__gui_element.gui, emd)
        self.__gui_element.load_element(gui_element)
        return gui_element

    def multi_element(self, emd):
        from arjuna.tpi.guiauto.template.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(self.__gui_element.gui, emd)
        self.__gui_element.load_multielement(m_guielement)
        return m_guielement

class GuiElementFinder:

    def __init__(self, gui_element):
        self.__emd_finder = GuiElementEmdFinder(gui_element)
        self.__gui_element = gui_element

    def locate(self, locator):
        from arjuna import log_debug
        from arjuna.tpi.exceptions import ArjunaTimeoutError, GuiElementNotPresentError
        emd = locator.as_emd()
        log_debug("Finding element with emd: {}.".format(emd))
        try:
            return getattr(self.__emd_finder, emd.meta["template"].name.lower())(emd)
        except ArjunaTimeoutError:
            raise GuiElementNotPresentError(self.__gui_element.gui, self.__gui_element)          

    def __locate_interim(self, name):
        def finder(fargs=None, **kwargs):
            locator = Locator(template=name, fmt_args=None, **kwargs)
            return self.locate(locator)
        return finder

    def __getattr__(self, name):
        return self.__locate_interim(name)