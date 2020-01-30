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

class GuiElement(ElementContainer, Locatable, Interactable):

    def __init__(self, gui, emd, iconfig=None):
        ElementContainer.__init__(self, gui.automator.config)
        Locatable.__init__(self, gui, emd) #, parent, obj_name="GuiElement")
        Interactable.__init__(self, gui, iconfig)

    def element(self, *str_or_with_locators, iconfig=None):
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        return element_with_lmd(self.gui, lmd, iconfig=iconfig)

    def element_with_lmd(self, gui, lmd, iconfig=None):
        from arjuna.interact.gui.auto.element.guielement import GuiElement
        gui_element = GuiElement(self.gui, lmd, iconfig=iconfig)
        self.load_element(gui_element)
        return gui_element        

    def multi_element(self, *str_or_with_locators, iconfig=None):
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        return self.multi_element_with_lmd(self.gui, lmd, iconfig=iconfig)

    def multi_element_with_lmd(self, gui, lmd, iconfig=None):
        from arjuna.interact.gui.auto.element.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(self.gui, lmd, iconfig=iconfig)
        self.load_multielement(m_guielement)
        return m_guielement

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")