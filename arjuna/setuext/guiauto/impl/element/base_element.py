import abc

from arjuna.setuext.guiauto.impl.base.element_container import ElementContainer
from arjuna.lib.enums import GuiElementConfigType

class BaseElement(ElementContainer, metaclass=abc.ABCMeta):
    def __init__(self, automator, emd, parent=None):
        super().__init__(automator.config)
        self.__automator = automator
        self.__parent = parent
        self.__emd = emd
        self.__found = False
        self.__located_by = None 
        self.dispatcher_creator = automator.dispatcher_creator

    @property
    def parent_container(self):
        return self.__parent and self.__parent or self.__automator

    def _create_element_flat_or_nested(self, locator_meta_data):
        from arjuna.setuext.guiauto.impl.element.guielement import GuiElement
        return GuiElement(self.__automator, locator_meta_data, parent=self) 

    def _create_multielement_flat_or_nested(self, locator_meta_data):
        from arjuna.setuext.guiauto.impl.element.multielement import GuiMultiElement
        return GuiMultiElement(self.__automator, locator_meta_data, parent=self) 

    def create_dispatcher(self):
        self._set_dispatcher(self.dispatcher_creator.create_gui_element_dispatcher(self.__automator.dispatcher, self.setu_id))

    @abc.abstractmethod
    def find_if_not_found(self):
        pass

    def get_locator_meta_data(self):
        return self.__emd

    def is_found(self):
        return self.__found

    def set_found_with(self, locator_type, locator_value):
        self.__found = True
        self.__located_by = locator_type, locator_value

    def get_found_with(self, locator_type, locator_value):
        return self.__located_by

    def get_automator(self):
        return self.__automator


class ElementConfig:

    def __init__(self, automator):
        self.__settings = {
            GuiElementConfigType.CHECK_TYPE: True,
            GuiElementConfigType.CHECK_PRE_STATE : True,
            GuiElementConfigType.CHECK_POST_STATE : True,
            }

    @property
    def settings(self):
        return self.__settings

    def __process_config_key(self, k):
        return type(k) is str and GuiElementConfigType[k.strip().upper()] or k

    def configure(self, settings):
        self.__settings.update({self.__process_config_key(k): v for k,v in settings.items()})

    def _should_check_type(self):
        return self.settings[GuiElementConfigType.CHECK_TYPE]

    def _should_check_pre_state(self):
        return self.settings[GuiElementConfigType.CHECK_PRE_STATE]

    def _should_check_post_state(self):
        return self.settings[GuiElementConfigType.CHECK_POST_STATE]



