from .base_element import BaseElement

class GuiElement(BaseElement):
    
    def __init__(self, automator, emd, parent=None):
        super().__init__(automator, emd, parent)
        from .element_conditions import GuiElementConditions
        self.__conditions_handler = GuiElementConditions(self)

    def find(self):
        self.parent_container.find_element(self)

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

    def get_tag_name(self):
        self.find_if_not_found()
        return self.__return_attr_value(self.dispatcher.get_tag_name())

    def get_attr_value(self, attr, optional=False):
        self.find_if_not_found()
        return self.__return_attr_value(self.dispatcher.get_attr_value(attr, optional))

    def get_text_content(self):
        self.find_if_not_found()
        return self.__return_attr_value(self.dispatcher.get_text_content())

    def click(self):
        self.find_if_not_found()
        self.wait_until_clickable()
        self._only_click()

    def __conditional_selected_state_click(self, condition_state):
        self.find_if_not_found()
        selected = self.is_selected()
        if selected == condition_state:
            self.wait_until_clickable()
            self._only_click()

    def select(self):
        self.__conditional_selected_state_click(False)

    def deselect(self):
        self.__conditional_selected_state_click(True)

    def wait_until_clickable(self):
        self.find_if_not_found()
        self.conditions.IsClickable().wait()

    def wait_until_visible(self):
        self.find_if_not_found()
        self.conditions.IsVisible().wait()

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

    def _only_clear_text(self):
        self.dispatcher.clear_text()

    def _only_enter_text(self, text):
        self._only_send_text(text)

    #################################
    ### Textbox abstraction
    #################################

    def clear_text(self):
        self.find_if_not_found()
        self.wait_until_clickable()
        self._only_click()
        self._only_clear_text()

    def enter_text(self, text):
        self.find_if_not_found()
        self.wait_until_clickable()
        self._only_click()
        self._only_enter_text(text)

    def set_text(self, text):
        self.find_if_not_found()
        self.wait_until_clickable()
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
