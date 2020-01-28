import random
import os

from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.dispatchable import Dispatchable
from arjuna.interact.gui.auto.base.configurable import Configurable
from arjuna.interact.gui.auto.element.guielement import GuiElement
from arjuna.interact.gui.auto.source.parser import *

class _GuiPartialElement(GuiElement):

    def __init__(self, gui, multi_element, index: int, dispatcher_element, iconfig=None):
        super().__init__(gui, multi_element.lmd, iconfig=iconfig)
        self.__multi_element = multi_element
        self.__index = index
        self.dispatcher = dispatcher_element

    def create_dispatcher(self):
        pass

    def _is_partial_element(self):
        return True

    @property
    def index(self):
        return self.__index

class GuiMultiElement(Locatable,Dispatchable,Configurable):
    
    def __init__(self, gui, lmd, iconfig=None): #, parent=None):
        Locatable.__init__(self, gui, lmd) #, parent)
        Dispatchable.__init__(self)
        Configurable.__init__(self, gui, iconfig)
        self.__instance_count = 0
        self.__instances = None
        self.__source_parser = None

        

    # def configure_partial_elements(self, elem_config):
    #     '''
    #         This method is supposed to be called when multielement identification is completed.
    #         This is not used for usual multi-element.
    #         It is used by RadioGroup or DropDown etc which are higher level abstractions that use ME.
    #     '''
    #     for instance in self.__instances:
    #         instance.configure(elem_config)

    # def find(self):
    #     self.parent_container.find_multielement(self)
    #     self.__load_source_parser()

    # #Override
    # def find_if_not_found(self):
    #     if not self.is_found():
    #         self.find()

    def load_source_parser(self):
        self.__source_parser = MultiElementSource()
        for instance in self.__instances:
            instance.load_source_parser()
        self.__source_parser.load(self.__instances)

    def __getitem__(self, index):
        # self.find_if_not_found()
        return self.__instances[index]

    @property
    def instance_count(self):
        # self.find_if_not_found()
        return self.__instance_count

    @instance_count.setter
    def instance_count(self, count):
        self.__instance_count = count
        self.__instances = [_GuiPartialElement(self.gui, self, i, self.dispatcher.get_element_at_index(i), iconfig=self.settings) for i in range(self.instance_count)]

    length = instance_count

    @property
    def random_element(self):
        # self.find_if_not_found()
        return self[random.randint(0, self.instance_count-1)]

    @property
    def first_element(self):
        return self[0]

    @property
    def last_element(self):
        return self[self.length-1]

    def get_element_at_ordinal(self, ordinal):
        # self.find_if_not_found()
        return self.__instances[ordinal-1]

    def get_instance_by_visible_text(self, text):
        texts = self.__get_all_texts()
        first_index = self.__find_first_text_index(texts, text)
        return self[first_index]

    def get_instance_by_value(self, value):
        values = self.__get_all_values()
        first_index = self.__find_first_value_index(values, value)
        return self[first_index]

    def wait_until_visible(self):
        self.find_if_not_found()
        # Should the logic be keptin Setu itself for this????

    def __return_attr_values(self, response):
        if "data" in response and "attrValues" in response["data"]:
            return response["data"]["attrValues"]
        else:
            return None

    def are_selected(self):
        return [instance.is_selected() for instance in self.__instances]

    # getting index attribute when it does not exist retursn value attribute.
    # So, not going the Selenium way. Setu would treat index as computer counting.
    def has_index_selected(self, index):
        # self.find_if_not_found()
        return self[index].is_selected()

    # Ordinal is human counting
    def has_ordinal_selected(self, ordinal):
        return self.has_index_selected(ordinal-1)

    def __find_first_match_index(self, in_sequence, to_match):
        try:
            return in_sequence.index(to_match)
        except:
            return -1

    def __get_all_texts(self):
        # self.find_if_not_found()
        self.load_source_parser()
        texts = self.__source_parser.get_text_contents()
        return texts

    def __find_first_text_index(self, texts, text):
        first_index = texts.index(text)
        if first_index == -1:
            raise Exception("No option with {} visible text present in drop down.".format(text))
        return first_index

    def __get_all_values(self):
        # self.find_if_not_found()
        self.load_source_parser()
        values = self.__source_parser.get_values()
        return values

    def __find_first_value_index(self, values, value):
        first_index = values.index(value)
        if first_index == -1:
            raise Exception("No option with {} value present in drop down.".format(value))
        return first_index

    def get_first_selected_instance(self):
        # self.find_if_not_found()
        self.load_source_parser()
        booleans = self.are_selected()
        first_index = None
        try:
            first_index = booleans.index(True)
        except:
            raise Exception("No option in drop down is currenlty selected.")
        else:
            return self[first_index]

    @property
    def source(self):
        return self.__source_parser
