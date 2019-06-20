from arjuna.setu.types import SetuManagedObject
from arjuna.setuext.guiauto.impl.element.guielement import GuiElement
from arjuna.setuext.guiauto.impl.locator.emd import SimpleGuiElementMetaData

# UUID is for client reference. Agent does not know about this.
class GuiWebSelect(SetuManagedObject):

    def __init__(self, automator, locator_meta_data, parent=None):
        super().__init__()
        self._wrapped_main_element = automator.create_element(locator_meta_data)
        tag = self._wrapped_main_element.get_tag_name()
        if tag.lower() != "select":
            raise Exception("The element should have a 'select' tag for WebSelect element. Found: " + tag)
        self._multi = self.__is_multi_select()
        self.__options = self._wrapped_main_element.create_multielement(
            SimpleGuiElementMetaData("tag_name", "option")
        )

    def __is_multi_select(self):
        return self._wrapped_main_element.get_attr_value("multiple", optional=True) is True or self._wrapped_main_element.get_attr_value("multi", optional=True) is True

    def is_multi_select(self):
        return self._multi

    def has_index_selected(self, index):
        return self.__options.get_instance_at_index(index).is_selected()

    def has_value_selected(self, value):
        return self.__options.get_instance_by_value(value).is_selected()

    def has_visible_text_selected(self, text):
        return self.__options.get_instance_by_visible_text(text).is_selected()

    def get_first_selected_option_text(self):
        option = self.__options.get_first_selected_instance()
        return option.get_text_content()

    def select_by_index(self, index):
        self.__options.get_instance_at_index(index).select()

    def select_by_ordinal(self, ordinal):
        return self.select_by_index(ordinal-1)

    def select_by_visible_text(self, text):
        return self.__options.get_instance_by_visible_text(text).select()

    def select_by_value(self, value):
        return self.__options.get_instance_by_value(value).select()

    # The following methods deal with multi-select and would be implemented later.

    def __validate_multi_select(self):
        if not self.is_multi_select():
            raise Exception("Deselect actions are allowed only for a multi-select dropdown.")

    def deselect_by_value(self, value):
        self.__validate_multi_select()
        return self.__options.get_instance_by_value(value).deselect()

    def deselect_by_index(self, index):
        pass

    def deselect_by_visible_text(self, text):
        pass

    def get_selected_options(self):
        pass

    def are_visible_texts_selected(self, text_list):
        pass

    def are_values_selected(self, text_list):
        pass

    def all_options(self):
        pass

    def select_by_values(self, value_list):
        pass

    def deselect_by_values(self, value_list):
        pass

    def select_by_indices(self, indices):
        pass

    def deselect_by_indices(self, indices):
        pass

    def select_by_visible_texts(self, text_list):
        pass

    def deselect_by_visible_texts(self, text_list):
        pass