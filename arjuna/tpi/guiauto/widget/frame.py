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

from arjuna.interact.gui.auto.finder.wmd import SimpleGuiWidgetMetaData
from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition

from arjuna.tpi.guiauto.source.element import GuiElementSource
from arjuna.tpi.tracker import track
from arjuna.tpi.guiauto.model.gns import GNS

@track("debug")
class GuiFrame:
    '''
        Represents an IFrame the Gui.

        Not meant to be directly created. It is created using calls from **Gui** object or **GuiNamespace** object of **Gui**.

        Arguments:
            gui: **Gui** object containing this GuiDropDown.
            wmd: **GuiElementMetaData** object for this GuiDropDown.

        Keyword Arguments:
            parent: **GuiElement** in case it is found inside a **GuiElement**. Default is the **Gui** object.
    '''

    def __init__(self, gui, wmd, parent=None):
        self.__gui = gui
        self.__wmd = wmd
        self.__automator = gui._automator
        self.__frame_finder = parent and parent or gui
        from arjuna.tpi.guiauto.model.app import GuiApp
        from arjuna.tpi.guiauto.model.page import GuiPage
        from arjuna.tpi.guiauto.model.section import GuiSection

        # If Gui is an app, then it falls back to App's finding mechanism.
        # If Gui is an GuiPage, then it falls back to GuiPage's finding mechanism.
        # If Gui is an GuiSection, then it falls back to main GuiPage's finding mechanism.
        # This is because GuiSection might use nested element finding which will not work inside frame content.
        if isinstance(gui, GuiApp):
            self.__finder = gui.app
        elif isinstance(gui, GuiPage):
            self.__finder = gui
        elif isinstance(gui, GuiSection):
            self.__finder = gui.parent
        else:
            raise Exception("Unrecognized container GUI for Frame. Expecting App/Page/Section. Found: {}".format(gui))

        frame_element = self.__frame_finder._wmd_finder.element(wmd)
        self.__automator.dispatcher.switch_to_frame(frame_element.dispatcher)

        # Frame has new DOM. Hence it uses the GuiPage to do the finding and is dependent on GuiPage's GNS as well.
        self.__gns = GNS(self.__finder, self.__finder._gui_def)

    def exit(self):
        self.__automator.browser.switch_to_dom_root()

    @property
    def gns(self):
        '''
            Gui Namespace (GNS) object for this GuiFrame.
        '''
        return self.__gns

    @property
    def _wmd(self):
        return self.__wmd

    @property
    def gui(self) -> 'Gui':
        '''
            **Gui** object containing this GuiFrame.
        '''
        return self.__gui

    @property
    def source(self) -> GuiElementSource:
        '''
            **GuiSource** for this GuiDropDown (source of root element).
        '''
        return self._wrapped_main_element.source

    def locate(self, locator):
        '''
           Locate a GuiWidget.

           Arguments:
            locator: `GuiWidgetDefinition` object.

            Returns:
                An object of type `GuiWidget`. Exact object type depends on the value of **type** attribute in `GuiWidgetDefinition`. 
        '''
        return self.__finder.locate(locator)

    def element(self, *, fargs=None, **kwargs) -> 'GuiElement':
        '''
            Locate a `GuiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiElement` object.
        '''
        return self.__finder.element(*fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs) -> 'GuiMultiElement':
        '''
            Locate a `GuiMultiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiMultiElement` object.
        '''
        return self.__finder.multi_element(*fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs) -> 'GuiDropDown':
        '''
            Locate a `GuiDropDown`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiDropDown` object.
        '''
        return self.__finder.dropdown(*fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs) -> 'GuiRadioGroup':
        '''
            Locate a `GuiRadioGroup`

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiRadioGroup` object
        '''
        return self.__finder.radio_group(*fargs, **kwargs)