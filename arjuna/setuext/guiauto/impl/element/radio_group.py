from arjuna.setu.types import SetuManagedObject
from .multielement import GuiMultiElement

# UUID is for client reference. Agent does not know about this.
class GuiWebRadioGroup(SetuManagedObject):

    def __init__(self, element_container, locator_meta_data):
        super().__init__()
        self._radios = element_container.create_multielement(locator_meta_data)
        self._validate_radio_buttons()

    def _validate_radio_buttons(self):
        tags = self._radios.get_tag_names()
        if [t for t in tags if t.strip().lower() != 'input']:
            raise Exception("Not a valid radio group. Contains non-input elements.")
        types = self._radios.get_attr_values("type")
        if [t for t in types if t.strip().lower() != 'radio']:
            raise Exception("Not a valid radio group. Contains non-radio elements.")
        names = self._radios.get_attr_values("name")
        refer_name = names[0]
        if [n for n in names if n != refer_name]:
            raise Exception("Not a valid radio group. Contains radio elements belonging to different radio groups.")

    def has_index_selected(self, index):
        return self._radios.get_instance_at_index(index).is_selected()

    def has_value_selected(self, value):
        return self._radios.get_instance_by_value(value).is_selected()

    def get_first_selected_option_value(self):
        instance = self._radios.get_first_selected_instance()
        return instance.get_attr_value("value")

    def select_by_index(self, index):
        self._radios.get_instance_at_index(index).select()

    def select_by_ordinal(self, ordinal):
        return self.select_by_index(ordinal-1)

    def select_by_value(self, value):
        return self._radios.get_instance_by_value(value).select()