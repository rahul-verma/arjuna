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

    def element(self, gui, lmd, iconfig=None):
        from arjuna.interact.gui.auto.element.guielement import GuiElement
        gui_element = GuiElement(gui, lmd, iconfig=iconfig)
        self.load_element(gui_element)
        return gui_element        

    def __multi_element(self, *str_or_with_locators, iconfig=None):
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        return self.multi_element(self.gui, lmd, iconfig=iconfig)

    def multi_element(self, gui, lmd, iconfig=None):
        from arjuna.interact.gui.auto.element.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(gui, lmd, iconfig=iconfig)
        self.load_multielement(m_guielement)
        return m_guielement

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def locate_with(self, *, template="element", **kwargs):
        from arjuna import Arjuna
        from arjuna.interact.gui.helpers import WithType, With
        with_list = []
        for k,v in kwargs.items():
            if k.upper() in WithType.__members__:
                with_list.append(getattr(With, k.lower())(v))
        if not with_list:
            raise Exception("You must provide atleast one locator.")
        from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData
        emd = GuiElementMetaData.create_lmd(*with_list)
        Arjuna.get_logger().debug("Finding element with emd: {}.".format(emd))
        return getattr(self, emd.meta.template.name.lower())(self.gui, emd)