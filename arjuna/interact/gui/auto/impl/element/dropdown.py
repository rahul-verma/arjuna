from arjuna.interact.gui.auto.impl.element.guielement import GuiElement
from arjuna.interact.gui.auto.impl.locator.emd import SimpleGuiElementMetaData
from .base_element import ElementConfig

# UUID is for client reference. Agent does not know about this.
class GuiWebSelect(ElementConfig):

    def __init__(self, automator, emd, parent=None, option_container_lmd=None, option_lmd=None):
        super().__init__(automator)
        self.__automator = automator
        self._wrapped_main_element = automator.define_element(emd)
        self.__found = False
        self.__options = None
        self.__option_lmd = option_lmd is not None and option_lmd or SimpleGuiElementMetaData("tag_name", "option")

        # It is seen in some websites like Bootstrap based that both select and options are children of a main div element.
        self.__option_container_same_as_select = option_container_lmd is None and True or False
        if not self.__option_container_same_as_select:
            self.__option_container = self.__automator.define_element(option_container_lmd)
            # Needs to be loaded so that options can be discovered.
            self.__option_container.find_if_not_found()

        self.__source_parser = None

    def __validate_select_control(self, tag):
        if tag.lower() != "select":
            raise Exception("The element should have a 'select' tag for WebSelect element. Found: " + tag)
        self._multi = self.__is_multi_select()

    def __get_root_element(self):
        return self.__option_container_same_as_select and self._wrapped_main_element or self.__option_container

    def __load_options(self):
        container = self.__get_root_element()
        self.__options = container.define_multielement(self.__option_lmd)
        self.__options.find_if_not_found()

    def is_found(self):
        return self.__found

    def __check_type_if_configured(self, tag):
        if self._should_check_type(): self.__validate_select_control(tag)

    def __find_if_not_found(self):
        if not self.is_found():
            # This would force the identification of partial elements in the wrapped multi-element.
            self._wrapped_main_element.configure(self.settings)
            self._wrapped_main_element.find()
            tag = self._wrapped_main_element.get_source(refind=False).get_tag_name()
            self.__check_type_if_configured(tag)
            self.__load_options()
            self.__options.configure_partial_elements(self.settings)
            self.__found = True

    def __is_multi_select(self):
        source = self._wrapped_main_element.get_source(refind=False)
        return source.get_attr_value("multiple", optional=True) is True or source.get_attr_value("multi", optional=True) is True

    def is_multi_select(self):
        return self._multi

    def __set_option_locators(self, emd):
        self.__option_lmd = emd

    def has_index_selected(self, index):
        self.__find_if_not_found()
        return self.__options.get_instance_at_index(index).is_selected()

    def has_value_selected(self, value):
        self.__find_if_not_found()
        return self.__options.get_instance_by_value(value).is_selected()

    def has_visible_text_selected(self, text):
        self.__find_if_not_found()
        return self.__options.get_instance_by_visible_text(text).is_selected()

    def get_first_selected_option_text(self):
        self.__find_if_not_found()
        option = self.__options.get_first_selected_instance()
        return option.get_source().get_text_content()

    def get_first_selected_option_value(self):
        self.__find_if_not_found()
        option = self.__options.get_first_selected_instance()
        return option.get_source().get_attr_value("value")

    def __select_option(self, option):
        self._wrapped_main_element.click()
        option.select()
        if self._should_check_post_state() and not option.is_selected():
            raise Exception("The attempt to select the dropdown option was not successful.")

    def select_by_index(self, index):
        self.__find_if_not_found()
        option = self.__options.get_instance_at_index(index)
        self.__select_option(option)

    def select_by_ordinal(self, ordinal):
        self.__find_if_not_found()
        return self.select_by_index(ordinal-1)

    def select_by_visible_text(self, text):
        self.__find_if_not_found()
        option = self.__options.get_instance_by_visible_text(text)
        self.__select_option(option)

    def send_option_text(self, text):
        self.__find_if_not_found()
        self._wrapped_main_element.send_text(text)

    def select_by_value(self, value):
        self.__find_if_not_found()
        option = self.__options.get_instance_by_value(value)
        self.__select_option(option)

    # The following methods deal with multi-select and would be implemented later.

    def __validate_multi_select(self):
        if not self.is_multi_select():
            raise Exception("Deselect actions are allowed only for a multi-select dropdown.")

    def deselect_by_value(self, value):
        self.__find_if_not_found()
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

    def get_source(self):
        self.__find_if_not_found()
        return self.__get_root_element().get_source()