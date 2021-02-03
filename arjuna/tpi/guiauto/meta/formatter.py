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

from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition
from arjuna.tpi.tracker import track

@track("trace")
class GNSLabelFormatter:
    '''
        Formattter for the GuiWidgetDefinition associated with a GNS Label.

        It is not created directly by a test author. Created using **.format** call of GNS object associated with a **Gui**.

        Args:
            gns: Gui Namespace object

        Keyword Arguments:
            **fargs: Arbitrary key-value pairs to format the GuiWidgetDefinition associated with a GNS Label.

        Note:
            Supports **.** notation for a **GuiWidgetLabel** just like a **GNS** object. For example:

                .. code-block:: python

                    fmt.label1
    '''

    def __init__(self, gns, **fargs):
        self.__gns = gns
        self.__gui_def = gns._get_gui_def()
        self.__fargs = fargs

    def __getattr__(self, name):
        wmd = self.__gui_def.get_wmd(name)
        from arjuna import log_debug
        log_debug("Finding element with label: {}, wmd: {} and fargs: {}".format(name, wmd, self.__fargs))
        fmt_wmd = wmd.create_formatted_wmd(**self.__fargs)
        for k,v in fmt_wmd.meta.relations.items():
            from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
            if type(v) is str:
                log_debug("Formatting related label {} in relations dict.".format(k))
                rwmd = self.__gui_def.get_wmd(v)
                log_debug("Retrieved  GuiWidgetMetaData {} for label {} in relations dict.".format(rwmd, k))
                log_debug("Formatting with args: {}".format(self.__fargs))
                frwmd = rwmd.create_formatted_wmd(**self.__fargs)
                fmt_wmd.meta.relations[k] = self.__gns._locate_with_wmd(frwmd).dispatcher.driver_element
                log_debug("Replaced label {} with corresponding GuiElement in relations dict.".format(k, frwmd))
        return self.__gns._locate_with_wmd(fmt_wmd)

@track("trace")
class GuiWidgetDefinitionFormatter:
    '''
        Formattter for a GuiWidgetDefinition created by GuiWidget factory methods.

        It is not created directly by a test author. Created using **.format** call of a **Gui** or **GuiElement**.

        Args:
            creator: **Gui** or **GuiElement**

        Keyword Arguments:
            **fargs: Arbitrary key-value pairs to format the GuiWidgetDefinition associated with a GNS Label.

        Note:
            Supports all GuiWidget factory method calls:

                .. code-block:: python

                    fmt.element
                    fmt.multi_element
                    fmt.dropdown
                    fmt.radio_group
    '''

    _FACTORIES = {"element", "multi_element", "dropdown", "radio_group"}

    def __init__(self, creator, **fargs):
        self.__creator = creator
        self.__fargs = fargs

    def locator(type="element", **kwargs) -> GuiWidgetDefinition:
        '''
            Create a GuiWidgetDefinition.

            Keyword Arguments:
                type: type of GuiWidget (element, multi_element, dropdown, radio_group)
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Returns:
                A `GuiWidgetDefinition` as per the arguments to this call and format arugments of this GuiWidgetDefinitionFormatter.

            Note:
                The format key-value pairs of this `GuiWidgetDefinitionFormatter` are used to format the identifiers in the constructed **GuiWidgetDefinition**.
        '''        

    def locate(self, type="element", **kwargs):
        '''
            Locate a GuiWidget.

            Keyword Arguments:
                type: type of GuiWidget (element, multi_element, dropdown, radio_group)
                **kwargs: Arbitrary key-value pairs used to construct a **GuiWidgetDefinition**

            Returns:
                An object of type `GuiWidget`. Exact object type depends on the value of **type** attribute. 

            Note:
                The format key-value pairs of this `GuiWidgetDefinitionFormatter` are used to format the identifiers in the constructed **GuiWidgetDefinition**.
        '''
        return self.__creator.locate(GuiWidgetDefinition(type=type, fmt_args=self.__fargs, **kwargs))

    def __getattr__(self, factory):
        if factory not in self._FACTORIES:
            raise Exception("Unsupported method for Formatter: {}. Allowed: {}.".format(factory, self._FACTORIES))
        from functools import partial
        return partial(getattr(self.__creator, factory), fargs=self.__fargs)

