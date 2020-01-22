from .base_element import BaseElement, ElementConfig
from arjuna.interact.gui.auto.impl.source.parser import ElementXMLSourceParser

class GuiElement(BaseElement, ElementConfig):
    
    def __init__(self, automator, emd, parent=None):
        BaseElement.__init__(self, automator, emd, parent, obj_name="GuiElement")
        ElementConfig.__init__(self, automator)
        from .element_conditions import GuiElementConditions, GuiElementLenientInteraction
        self.__conditions_handler = GuiElementConditions(self)
        self.__interaction_handler = GuiElementLenientInteraction(self)
        self.__source_parser = None
        self.__automator = automator

    def __get_attr_value_from_remote(self, attr, optional=False):
        return self.__return_attr_value(self.dispatcher.get_attr_value(attr, optional))

    def get_source_from_remote(self):
        return self.__get_attr_value_from_remote("outerHTML")

    def load_source_parser(self):
        raw_source = self.get_source_from_remote()
        if self.__source_parser is None:
            self.__source_parser = ElementXMLSourceParser(self)
        self.__source_parser.load()

    def find(self):
        self.parent_container.find_element(self)

    def find_without_wait(self):
        self.parent_container.find_element_without_wait(self)

    identify = find

    #Override
    def find_if_not_found(self):
        if not self.is_found():
            self.find()

    def _is_partial_element(self):
        return False

    def _get_instance_number(self):
        raise Exception("Instance number is applicable only for partial gui elements.")

    def __append_instance_number(self, d):
        if self._is_partial_element():
            d["isInstanceAction"] = True
            d["instanceIndex"] = self._get_instance_number()
        return d

    def _kwargs(self, **kwargs):
        return self.__append_instance_number(kwargs)

    def _noargs(self):
        return self.__append_instance_number({})

    def _only_send_text(self, text):
        self.dispatcher.send_text(text)

    def _only_click(self):
        self.dispatcher.click()

    def __return_attr_value(self, result):
        return result and result or None

    def click(self):
        self.find_if_not_found()
        self.__wait_until_clickable_if_configured()
        self.interactions.Click().wait()
        #self._only_click()

    def __only_hover(self):
        self.dispatcher.hover()

    def hover(self):
        self.find_if_not_found()
        self.__wait_until_clickable_if_configured()
        self.__only_hover()

    def __conditional_selected_state_click(self, condition_state):
        self.find_if_not_found()
        selected = self.is_selected()
        if selected == condition_state:
            self.__wait_until_clickable_if_configured()
            self._only_click()

    def select(self):
        self.__conditional_selected_state_click(False)

    def deselect(self):
        self.__conditional_selected_state_click(True)

    wait_until_present = find

    def wait_until_visible(self):
        self.find_if_not_found()
        self.conditions.IsVisible().wait()

    def wait_until_clickable(self):
        self.find_if_not_found()
        self.conditions.IsClickable().wait()

    def wait_until_selected(self):
        self.find_if_not_found()
        self.conditions.IsVisible().wait()

    #################################
    ### State Checking
    #################################
    def is_selected(self):
        self.find_if_not_found()
        return self.dispatcher.is_selected()

    def is_visible(self):
        self.find_if_not_found()
        return self.dispatcher.is_visible()

    def is_clickable(self):
        self.find_if_not_found()
        return self.dispatcher.is_clickable()

    @property
    def conditions(self):
        return self.__conditions_handler

    @property
    def interactions(self):
        return self.__interaction_handler

    def _only_clear_text(self):
        self.dispatcher.clear_text()

    def _only_enter_text(self, text):
        self._only_send_text(text)

    #################################
    ### Textbox abstraction
    #################################

    def clear_text(self):
        self.find_if_not_found()
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_clear_text()

    def send_text(self, text):
        self.find_if_not_found()
        self.__wait_until_clickable_if_configured()
        self._only_enter_text(text)

    def enter_text(self, text):
        self.find_if_not_found()
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_enter_text(text)

    def set_text(self, text):
        self.find_if_not_found()
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_clear_text()
        self._only_enter_text(text)

    def has_entered_text(self, text):
        pass

    def has_entered_partial_text(self, text):
        pass

    #################################
    ### Checkbox abstraction
    #################################
    def check(self):
        self.select()

    def uncheck(self):
        self.deselect()

    def toggle_checkbox(self):
        self.click()

    def is_checked(self):
        return self.is_selected()

    def __wait_until_clickable_if_configured(self):
        if self._should_check_pre_state(): self.wait_until_clickable()

    def get_source(self, refind=True, reload=True):
        if refind:
            self.find_if_not_found()
        if reload:
            self.load_source_parser()
        return self.__source_parser

    def get_property_value(self, attr):
        self.find_if_not_found()
        return self.__get_attr_value_from_remote(attr)

    def perform_action_chain(self, single_action_chain):
        from arjuna.interact.gui.auto.automator.actions import SingleActionChain
        action_chain = SingleActionChain(self.__automator, element=self)
        action_chain.perform(single_action_chain)

    def find_element_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

    def find_multielement_with_js(self, js):
        raise Exception("With.JS is currently not supported for nested element finding.")

