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


from arjuna.tpi.guiauto.base.locatable import Locatable
from arjuna.tpi.guiauto.base.single_widget import SingleGuiWidget
from arjuna.tpi.guiauto.base.container import GuiWidgetContainer
from arjuna.tpi.engine.asserter import AsserterMixIn
from arjuna.tpi.guiauto.model.gns import GNS
from arjuna.interact.gui.auto.finder import GuiElementFinder, GuiElementEmdFinder
from arjuna.tpi.error import *
from arjuna.core.error import *
from arjuna.tpi.tracker import track
from arjuna.tpi.guiauto.meta.formatter import GuiWidgetDefinitionFormatter

@track("debug")
class GuiElement(AsserterMixIn, GuiWidgetContainer, Locatable, SingleGuiWidget):
    '''
        Represents a single element in GUI of any kind.

        Not meant to be directly created. It is created using calls from **Gui** object or **GuiNamespace** object of **Gui**.

        Arguments:
            gui: Gui object containing this element.
            wmd: **GuiElementMetaData** object for this element.
    '''

    def __init__(self, gui, wmd):
        AsserterMixIn.__init__(self)
        GuiWidgetContainer.__init__(self, gui._automator.config)
        Locatable.__init__(self, gui, wmd) #, parent, obj_name="GuiElement")
        SingleGuiWidget.__init__(self, gui, wmd)
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
        '''
            Gui Namespace (GNS) object for this GuiElement.
        '''
        return self.__gns

    @property
    def root_element(self):
        '''
            Root Element for this GuiElement.
        '''
        return None

    def _find_element_with_js(self, js):
        # Falls back to driver level
        return self._automator.dispatcher.find_element_with_js(js)

    def _find_multielement_with_js(self, js):
        # Falls back to driver level
        return self._automator.dispatcher.find_multielement_with_js(js)

    def _wait_until_absent(self, wmd):
        try:
            self._wait_until_element_absent(wmd)
        except ArjunaTimeoutError:
            raise GuiWidgetPresentError(self.gui, wmd) 

    def wait_until_absent(self, *, fargs=None, **kwargs):
        '''
            Wait until a **GuiWidget** is absent inside this GuiElement.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the **GuiWidgetDefinition**. Use **.format(**kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Note:
                By default Wait is done until **ArjunaOption.GUIAUTO_MAX_WAIT** in the **Configuration** object associated with this **GuiElement**.

                You can pass **max_wait** argument to change this. Value is considered in seconds.
        '''
        from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition
        wmd = GuiWidgetDefinition(fmt_args=fargs, **kwargs)._as_wmd()
        self._wait_until_absent(wmd)

    def contains(self, *, fargs=None, **kwargs):
        '''
            Check whether this GuiElement object contains a **GuiWidget**. Includes dynamic waiting.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the **GuiWidgetDefinition**. Use **.format(**kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Note:
                By default Wait is done until `ArjunaOption.GUIAUTO_MAX_WAIT` in the **Configuration** object associated with this **GuiElement**.

                You can pass **max_wait** argument to change this. Value is considered in seconds.
        '''
        try:
            self.element(fargs=fargs, **kwargs)
        except GuiWidgetNotPresentError:
            return False
        else:
            return True

    ########## Served by Template ########

    def formatter(self, **fargs) -> GuiWidgetDefinitionFormatter:
        '''
            Create a :class:`~arjuna.tpi.guiauto.meta.formatter.GuiWidgetDefinitionFormatter` object.

            Keyword Arguments:
                **fargs: Arbitrary key-value pairs to be used for formatting identifiers in **GuiWidgetDefinition**.
        '''
        return GuiWidgetDefinitionFormatter(self, **fargs)

    def locate(self, locator):
        '''
           Locate a `GuiWidget`.

           Arguments:
            locator: `GuiWidgetDefinition` object.

            Returns:
                An object of type `GuiWidget`. Exact object type depends on the value of **type** attribute in **GuiWidgetDefinition**. 
        '''
        return self._finder.locate(locator)

    def element(self, *, fargs=None, **kwargs):
        '''
            Locate a `GuiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the **GuiWidgetDefinition**. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Returns:
                `GuiElement` object.
        '''
        return self._finder.element(fargs=fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs):
        '''
            Locate a `GuiMultiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the **GuiWidgetDefinition**. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Returns:
                `GuiMultiElement` object.
        '''
        return self._finder.multi_element(fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs):
        '''
            Locate a `GuiDropDown`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the **GuiWidgetDefinition**. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Returns:
                `GuiDropDown` object.
        '''
        return self._finder.dropdown(fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs):
        '''
            Locate a `GuiRadioGroup`

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the **GuiWidgetDefinition**. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Returns:
                `GuiRadioGroup` object
        '''
        return self._finder.radio_group(fargs=fargs, **kwargs)