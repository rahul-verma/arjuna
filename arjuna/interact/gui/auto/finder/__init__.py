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
from arjuna.tpi.error import *
from arjuna.core.error import *
from arjuna.tpi.guiauto.meta.locator import GuiWidgetLocator

class GuiEmdFinder:

    def __init__(self, gui):
        self.__gui = gui
        self.__automator = gui._automator

    def __getattr__(self, name):
        return partial(getattr(self.__automator, name.lower()), self.__gui)

class GuiFinder:

    def __init__(self, gui):
        self.__wmd_finder = GuiEmdFinder(gui)
        self.__gui = gui

    def locate(self, locator):
        from arjuna import log_debug
        from arjuna.core.error import ArjunaTimeoutError
        from arjuna.tpi.error import GuiWidgetNotPresentError
        
        wmd = locator._as_wmd()
        log_debug("Finding element with wmd: {}.".format(wmd))
        try:
            return getattr(self.__wmd_finder, wmd.meta["type"].name.lower())(wmd)
        except ArjunaTimeoutError:
            raise GuiWidgetNotPresentError(self.__gui, wmd)         

    def __locate_interim(self, name):
        def finder(fargs=None, **kwargs):
            locator = GuiWidgetLocator(type=name, fmt_args=fargs, **kwargs)
            return self.locate(locator)
        return finder

    def __getattr__(self, name):
        return self.__locate_interim(name)

class GuiElementEmdFinder:

    def __init__(self, gui_element):
        self.__gui_element = gui_element

    def element(self, wmd):
        from arjuna.tpi.guiauto.widget.element import GuiElement
        gui_element = GuiElement(self.__gui_element.gui, wmd)
        self.__gui_element._load_element(gui_element)
        return gui_element

    def multi_element(self, wmd):
        from arjuna.tpi.guiauto.widget.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(self.__gui_element.gui, wmd)
        self.__gui_element._load_multielement(m_guielement)
        return m_guielement

class GuiElementFinder:

    def __init__(self, gui_element):
        self.__wmd_finder = GuiElementEmdFinder(gui_element)
        self.__gui_element = gui_element

    def locate(self, locator):
        from arjuna import log_debug
        from arjuna.core.error import ArjunaTimeoutError
        from arjuna.tpi.error import GuiWidgetNotPresentError

        wmd = locator._as_wmd()
        log_debug("Finding element with wmd: {}.".format(wmd))
        try:
            return getattr(self.__wmd_finder, wmd.meta["type"].name.lower())(wmd)
        except ArjunaTimeoutError:
            raise GuiWidgetNotPresentError(self.__gui_element.gui, self.__gui_element)          

    def __locate_interim(self, name):
        def finder(fargs=None, **kwargs):
            locator = GuiWidgetLocator(type=name, fmt_args=None, **kwargs)
            return self.locate(locator)
        return finder

    def __getattr__(self, name):
        return self.__locate_interim(name)