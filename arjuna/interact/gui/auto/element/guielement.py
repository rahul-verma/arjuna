from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.interactable import Interactable
from arjuna.interact.gui.auto.base.container import ElementContainer

class GuiElement(ElementContainer, Locatable, Interactable):

    def __init__(self, gui, emd):
        ElementContainer.__init__(self, gui.automator.config)
        Locatable.__init__(self, gui, emd) #, parent, obj_name="GuiElement")
        Interactable.__init__(self, gui)

    def element(self, *str_or_with_locators):
        from arjuna.interact.gui.auto.element.guielement import GuiElement
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        gui_element = GuiElement(self.gui, lmd)
        self.load_element(gui_element)
        return gui_element

    def multi_element(self, *str_or_with_locators):
        from arjuna.interact.gui.auto.element.multielement import GuiMultiElement
        lmd = self.gui.convert_to_with_lmd(*str_or_with_locators)
        m_guielement = GuiMultiElement(self.gui, lmd)
        self.load_multielement(m_guielement)
        return m_guielement

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")