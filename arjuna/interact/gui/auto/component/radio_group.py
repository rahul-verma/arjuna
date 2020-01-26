from .multielement import GuiMultiElement
from .base_element import ElementConfig

# UUID is for client reference. Agent does not know about this.
class GuiWebRadioGroup(ElementConfig):

    def __init__(self, element_container, emd, parent=None):
        super().__init__(element_container)
        self._radios = element_container.define_multielement(emd)
        self.__found = False

    def __validate_radio_buttons(self, source):
        if [t for t in source.get_tag_names() if t.strip().lower() != 'input']:
            raise Exception("Not a valid radio group. Contains non-input elements.")
        if [t for t in source.get_attr_values("type") if t.strip().lower() != 'radio']:
            raise Exception("Not a valid radio group. Contains non-radio elements.")
        names = source.get_attr_values("name")
        if len(set(names)) != 1:
            raise Exception("Not a valid radio group. Contains radio elements belonging to different radio groups.")

    def is_found(self):
        return self.__found

    def __check_type_if_configured(self, tags):
        if self._should_check_type(): self.__validate_radio_buttons(tags)

    def __find_if_not_found(self):
        if not self.is_found():
            # This would force the identification of partial elements in the wrapped multi-element.
            self._radios.find()
            source = self._radios.get_source(refind=False)
            self.__check_type_if_configured(source)
            self._radios.configure_partial_elements(self.settings)
            self.__found = True

    def has_index_selected(self, index):
        self.__find_if_not_found()
        return self._radios.get_instance_at_index(index).is_selected()

    def has_value_selected(self, value):
        self.__find_if_not_found()
        return self._radios.get_instance_by_value(value).is_selected()

    def get_first_selected_option_value(self):
        self.__find_if_not_found()
        instance = self._radios.get_first_selected_instance()
        return instance.get_source(refind=False, reload=False).get_attr_value("value")

    def __select_option(self, option):
        option.select()
        if self._should_check_post_state() and not option.is_selected():
            raise Exception("The attempt to select the radio button was not successful.")

    def select_by_index(self, index):
        self.__find_if_not_found()
        option = self._radios.get_instance_at_index(index)
        self.__select_option(option)

    def select_by_ordinal(self, ordinal):
        self.__find_if_not_found()
        return self.select_by_index(ordinal-1)

    def select_by_value(self, value):
        self.__find_if_not_found()
        option = self._radios.get_instance_by_value(value)
        self.__select_option(option)

    def get_source(self):
        self.__find_if_not_found()
        return self._radios.get_source()