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


from .gui import Gui
from .content import GuiAppContent
from arjuna.interact.gui.auto.finder.wmd import GuiWidgetMetaData
from arjuna.tpi.tracker import track
from arjuna.tpi.guiauto.source.element import GuiElementSource

@track("debug")
class GuiSection(GuiAppContent):
    '''
        Represents a GUI Section i.e. a part of the current page in the Gui. 
        
        It is an implementation of **GuiAppContent**.

        Args:
            *args: Any number of positional argumnts. These are passed to the **prepare()** method if defined in inherited class.

        Keyword Arguments:
            parent_gui: (Mandatory) The **Gui** object that contains this **GuiSection**.
            label: Label for the this **GuiSection**. If not provided, the class name is used as the label.
            root: Root element of this **GuiSection**. Can be **label** string defined in its GNS File or a **Locator** object.
            gns_dir: Relative Root Directory for GNS file associated with this **GuiSection**. Default is **page/section** directory in associated **GuiApp** namespace. If provided, it is considered relative to the namespace directory of associated **GuiApp**.
            gns_file_name: Name of GNS file associated with this **GuiSection**. If not provided, default is **<label>.yaml**.
            kwargs: Arbitrary keyword arugments. These are passed to the **prepare()** method if defined in inherited class.

        Note:
            A **GuiSection** can have a root element. If defined, all locator calls in this object happen as a nested locating call using the root element.

                - Root element provided in in __init__ call is given preference.
                - If not provided, Arjuna looks for **root** definition in **load** section of its GNS file.
                - If above is also not provided, then locating happens from the root of the DOM of current page.
    '''

    def __init__(self, *args, parent_gui: Gui, label: 'str'=None, root: 'LabelOrLocator'=None, gns_dir: str=None, gns_file_name:str=None, **kwargs):
        super().__init__(automator=parent_gui._automator, label=label, gns_dir=gns_dir, gns_file_name=gns_file_name)   
        self.__root_meta = self.__determine_root(root)
        self.__root_element = None
        self.__container = self
        self._load(*args, **kwargs)
        self.__parent = parent_gui

    @property
    def _root_element(self):
        return self.__root_element

    def __determine_root(self, root_init):
        from arjuna import GuiWidgetDefinition
        root_label = None
        root_gns = self._gui_def.root_element_name
        if root_init:
            # root in __init__ as a Locator instead of GNS Label
            if isinstance(root_init, GuiWidgetDefinition):
                root_label = "anonymous"
            else:
                root_label = root_init
        else:
            root_label = root_gns
        from arjuna import log_debug
        log_debug("Setting Root Element for {} Gui. Label: {}. Root in GNS: {}. Root in __init__: {}.".format(
            self.label,
            root_label,
            root_gns,
            root_init
        ))

        if root_label:
            root_label = root_label.lower().strip()
            return root_label, root_init
        else:
            return None

    def _load_root_element(self):
        '''
            Loads root element for GuiSection.

            Root element is always loaded by using GuiPage. Rest of the elements are loaded as nested elements in root.
        '''
        if self.__root_meta:
            label, locator = self.__root_meta
            if self.__root_meta[0] != "anonymous":
                wmd = self._gui_def.get_wmd(label)
                from arjuna import log_debug
                log_debug("Loading Root Element {} for Gui GuiSection: {}".format(label, self.label))
                self.__root_element = self._wmd_finder.element(wmd)
            else:
                from arjuna import log_debug
                log_debug("Loading Root Element with Locator {} for Gui GuiSection: {}".format(str(locator), self.label))
                self.__root_element = self._finder.locate(locator)           
            
            self.__container = self.__root_element

    def __get_caller(self, name):
        if self.__container is self:
            return getattr(super(), name)
        else:
            return getattr(self.__container, name)

    def locate(self, locator):
        '''
           Locate a GuiWidget.

           Arguments:
            locator: `GuiWidgetDefinition` object.

            Returns:
                An object of type `GuiWidget`. Exact object type depends on the value of **type** attribute in `GuiWidgetDefinition`. 
        '''
        return self.__get_caller("locate")(fargs=fargs, **kwargs)

    def element(self, *, fargs=None, **kwargs) -> 'GuiElement':
        '''
            Locate a `GuiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiElement` object.
        '''
        return self.__get_caller("element")(fargs=fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs) -> 'GuiMultiElement':
        '''
            Locate a `GuiMultiElement`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiMultiElement` object.
        '''
        return self.__get_caller("multi_element")(fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs) -> 'GuiDropDown':
        '''
            Locate a `GuiDropDown`.

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiDropDown` object.
        '''
        return self.__get_caller("dropdown")(fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs) -> 'GuiRadioGroup':
        '''
            Locate a `GuiRadioGroup`

            Keyword Arguments:
                fargs: A dictionary of key-value pairs for formatting the `GuiWidgetDefinition`. Use **.format(kwargs).wait_until_absent** for more Pythonic code when formatting.
                **kwargs: Arbitrary key-value pairs used to construct a `GuiWidgetDefinition`

            Returns:
                `GuiRadioGroup` object
        '''
        return self.__get_caller("radio_group")(fargs=fargs, **kwargs)     

    @property
    def parent(self):
        '''
            Parent GUI of this **GuiSection**.
        '''
        return self.__parent

    @property
    def source(self) -> GuiElementSource:
        '''
           `GuiElementSource` object for the root element of this **GuiSection**.

           Raises:
            Exception is raised if root element is not defined.
        '''
        return self._automator.source