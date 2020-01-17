import abc

from arjuna.interact.gui.auto.impl.base.element_container import ElementContainer
from arjuna.core.enums import GuiActionConfigType

class BaseElement(ElementContainer, metaclass=abc.ABCMeta):
    def __init__(self, automator, emd, parent=None, obj_name=""):
        super().__init__(automator.config, obj_name)
        self.__automator = automator
        self.__parent = parent
        self.__lmd = emd
        self.__found = False
        self.__located_by = None 
        self.__dispatcher_element = None

    @property
    def automator(self):
        return self.__automator

    @property
    def dispatcher(self):
        return self.__dispatcher_element

    @dispatcher.setter
    def dispatcher(self, element):
        self.__dispatcher_element = element

    @property
    def parent_container(self):
        return self.__parent and self.__parent or self.__automator

    def _create_element_flat_or_nested(self, locator_meta_data):
        from arjuna.interact.gui.auto.impl.element.guielement import GuiElement
        return GuiElement(self.__automator, locator_meta_data, parent=self) 

    def _create_multielement_flat_or_nested(self, locator_meta_data):
        from arjuna.interact.gui.auto.impl.element.multielement import GuiMultiElement
        return GuiMultiElement(self.__automator, locator_meta_data, parent=self) 

    def create_dispatcher(self):
        self._set_dispatcher(self.dispatcher_creator.create_gui_element_dispatcher(self.__automator.dispatcher, self.setu_id))

    @abc.abstractmethod
    def find_if_not_found(self):
        pass

    def get_lmd(self):
        return self.__lmd

    def is_found(self):
        return self.__found

    def set_found_with(self, locator_type, locator_value):
        self.__found = True
        self.__located_by = locator_type, locator_value

    def get_found_with(self):
        return self.__located_by


class ElementConfig:

    def __init__(self, automator):
        self.__settings = {
            GuiActionConfigType.CHECK_TYPE: True,
            GuiActionConfigType.CHECK_PRE_STATE : True,
            GuiActionConfigType.CHECK_POST_STATE : True,
    }

    @property
    def settings(self):
        return self.__settings

    def configure(self, settings):
        self.__settings.update(settings)

    def _should_check_type(self):
        return self.settings[GuiActionConfigType.CHECK_TYPE]

    def _should_check_pre_state(self):
        return self.settings[GuiActionConfigType.CHECK_PRE_STATE]

    def _should_check_post_state(self):
        return self.settings[GuiActionConfigType.CHECK_POST_STATE]



