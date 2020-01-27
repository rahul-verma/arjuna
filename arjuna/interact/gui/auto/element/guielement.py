from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.interactable import Interactable
from arjuna.interact.gui.auto.base.container import ElementContainer

class GuiElement(ElementContainer, Locatable, Interactable):

    def __init__(self, automator, emd):
        ElementContainer.__init__(self, automator.config)
        Locatable.__init__(self, automator, emd) #, parent, obj_name="GuiElement")
        Interactable.__init__(self, automator)

    def element(self, lmd):
        from arjuna.interact.gui.auto.element.guielement import GuiElement
        gui_element = GuiElement(self, lmd) 
        self.load_element(gui_element)
        return gui_element

    def multi_element(self, lmd):
        from arjuna.interact.gui.auto.element.multielement import GuiMultiElement
        m_guielement = GuiMultiElement(self, lmd)
        self.load_multielement(m_guielement)
        return m_guielement

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")


########## to be removed after validation
'''
    #Override
    def find_if_not_found(self):
        if not self.is_found():
            self.find()


    def __append_instance_number(self, d):
        if self._is_partial_element():
            d["isInstanceAction"] = True
            d["instanceIndex"] = self._get_instance_number()
        return d


'''