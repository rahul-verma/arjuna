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


from .gui import *
from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData


class GuiSection(AppContent):

    def __init__(self, gui, *args, gns_dir=None, root=None, label=None, gns_file_name=None, **kwargs):
        super().__init__(automator=gui.automator, label=label, gns_dir=gns_dir, gns_file_name=gns_file_name)   
        self.__root_meta = self.__determine_root(root)
        self.__root_element = None
        self.__container = self
        self._load(*args, **kwargs)
        self.__parent = gui

    @property
    def root_element(self):
        return self.__root_element

    def __determine_root(self, root_init):
        from arjuna import Locator
        root_label = None
        root_gns = self.gui_def.root_element_name
        if root_init:
            # root in __init__ as a Locator instead of GNS Label
            if isinstance(root_init, Locator):
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
                emd = self.gui_def.get_emd(label)
                from arjuna import log_debug
                log_debug("Loading Root Element {} for Gui GuiSection: {}".format(label, self.label))
                self.__root_element = self.emd_finder.element(emd)
            else:
                from arjuna import log_debug
                log_debug("Loading Root Element with Locator {} for Gui GuiSection: {}".format(str(locator), self.label))
                self.__root_element = self.finder.locate(locator)           
            
            self.__container = self.__root_element

    def __get_caller(self, name):
        if self.__container is self:
            return getattr(super(), name)
        else:
            return getattr(self.__container, name)

    def locate(self, locator):
        return self.__get_caller("locate")(fargs=fargs, **kwargs)

    def element(self, *, fargs=None, **kwargs):
        return self.__get_caller("element")(fargs=fargs, **kwargs)

    def multi_element(self, fargs=None, **kwargs):
        return self.__get_caller("multi_element")(fargs=fargs, **kwargs)

    def dropdown(self, fargs=None, **kwargs):
        return self.__get_caller("dropdown")(fargs=fargs, **kwargs)

    def radio_group(self, fargs=None, **kwargs):
        return self.__get_caller("radio_group")(fargs=fargs, **kwargs)     

    @property
    def parent(self):
        return self.__parent

GuiWidget = GuiSection
GuiDialog = GuiSection
