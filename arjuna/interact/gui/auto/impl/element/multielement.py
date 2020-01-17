import random
import os

from arjuna.interact.gui.auto.impl.element.base_element import BaseElement
from arjuna.interact.gui.auto.impl.element.guielement import GuiElement
from arjuna.interact.gui.auto.impl.source.parser import *

class GuiMultiElement(BaseElement):
    
    def __init__(self, automator, emd, parent=None):
        super().__init__(automator, emd, parent)
        self.instance_count = 0
        self.__instances = None
        self.__source_parser = None

    def configure_partial_elements(self, elem_config):
        '''
            This method is supposed to be called when multielement identification is completed.
            This is not used for usual multi-element.
            It is used by RadioGroup or DropDown etc which are higher level abstractions that use ME.
        '''
        for instance in self.__instances:
            instance.configure(elem_config)

    def find(self):
        self.parent_container.find_multielement(self)

    #Override
    def find_if_not_found(self):
        if not self.is_found():
            self.find()

    def load_source_parser(self):
        if not self.__source_parser:
            self.__source_parser = MultiElementSource()
        for instance in self.__instances:
            instance.load_source_parser()
        self.__source_parser.load(self.__instances)

    def set_instance_count(self, count):
        self.instance_count = count
        self.__instances = [_GuiPartialElement(self.automator, self, i, self.dispatcher.get_element_at_index(i)) for i in range(self.instance_count)]

    def get_instance_count(self):
        self.find_if_not_found()
        return self.instance_count

    def get_random_index(self):
        self.find_if_not_found()
        return random.randint(0, self.instance_count-1)

    def get_instance_at_index(self, index):
        self.find_if_not_found()
        return self.__instances[index]

    def get_instance_at_ordinal(self, ordinal):
        self.find_if_not_found()
        return self.__instances[ordinal-1]

    def get_instance_by_visible_text(self, text):
        texts = self.__get_all_texts()
        first_index = self.__find_first_text_index(texts, text)
        return self.get_instance_at_index(first_index)

    def get_instance_by_value(self, value):
        values = self.__get_all_values()
        first_index = self.__find_first_value_index(values, value)
        return self.get_instance_at_index(first_index)

    def wait_until_visible(self):
        self.find_if_not_found()
        # Should the logic be keptin Setu itself for this????

    def __return_attr_values(self, response):
        if "data" in response and "attrValues" in response["data"]:
            return response["data"]["attrValues"]
        else:
            return None

    def are_selected(self):
        self.find_if_not_found()
        return [instance.is_selected() for instance in self.__instances]

    # getting index attribute when it does not exist retursn value attribute.
    # So, not going the Selenium way. Setu would treat index as computer counting.
    def has_index_selected(self, index):
        self.find_if_not_found()
        return self.get_instance_at_index(index).is_selected()

    # Ordinal is human counting
    def has_ordinal_selected(self, ordinal):
        return self.has_index_selected(ordinal-1)

    def __find_first_match_index(self, in_sequence, to_match):
        try:
            return in_sequence.index(to_match)
        except:
            return -1

    def __get_all_texts(self):
        self.find_if_not_found()
        self.load_source_parser()
        texts = self.__source_parser.get_text_contents()
        return texts

    def __find_first_text_index(self, texts, text):
        first_index = texts.index(text)
        if first_index == -1:
            raise Exception("No option with {} visible text present in drop down.".format(text))
        return first_index

    def __get_all_values(self):
        self.find_if_not_found()
        self.load_source_parser()
        values = self.__source_parser.get_values()
        return values

    def __find_first_value_index(self, values, value):
        first_index = values.index(value)
        if first_index == -1:
            raise Exception("No option with {} value present in drop down.".format(value))
        return first_index

    def get_first_selected_instance(self):
        self.find_if_not_found()
        self.load_source_parser()
        booleans = self.are_selected()
        first_index = None
        try:
            first_index = booleans.index(True)
        except:
            raise Exception("No option in drop down is currenlty selected.")
        else:
            return self.get_instance_at_index(first_index)

    def get_source(self, refind=True, reload=True):
        if refind:
            self.find_if_not_found()
        if reload:
            self.load_source_parser()
        return self.__source_parser

class _GuiPartialElement(GuiElement):

    def __init__(self, automator, multi_element: GuiMultiElement, instance_number: int, dispatcher_element):
        super().__init__(automator, multi_element)
        self.__multi_element = multi_element
        self.__instance_number = instance_number
        # dispatcher.set_partial(self.__instance_number)
        self.dispatcher = dispatcher_element

    def create_dispatcher(self):
        pass

    #Override
    def find_if_not_found(self):
        # Unlike regular item no attempt should be made to indepently identify a part element.
        pass

    def _is_partial_element(self):
        return True

    def _get_instance_number(self):
        return self.__instance_number