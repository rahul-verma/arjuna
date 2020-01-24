import os
from enum import Enum

from arjuna.tpi.guiauto.helpers import With
from arjuna.interact.gui.auto.invoker.component import GuiAutoComponentFactory
from arjuna.interact.gui.auto.impl.locator.emd import GuiElementMetaData
from arjuna.tpi.enums import ArjunaOption

class BaseGui:

    def __init__(self, automator, ns_dir, label=None, def_file_name=None, parent=None, register=True, multi_context=False):
        super().__init__()
        self.__automator = automator
        self.__children_map = dict()
        self.__gui_registered = False
        self.__parent = parent
        self.__impl_gui = None

        self.__label = None
        self.__def_file_name = None

        if label:
            self.set_label(label)
        else:
            self.set_label(self.__class__.__name__)

        if def_file_name:
            self.set_def_file_name(def_file_name)
        else:
            self.set_def_file_name("{}.gns".format(self.label))
        
        ns_root_dir = self.config.get_arjuna_option_value(ArjunaOption.GUIAUTO_NAMESPACE_DIR).as_str()
        self.__def_file_path = os.path.join(ns_root_dir, ns_dir, self.def_file_name)

        if register:
            self._register()

    @property
    def impl_gui(self):
        return self.__impl_gui

    @property
    def automator(self):
        return self.__automator

    @property
    def impl_automator(self):
        return self.automator.impl_automator

    @property
    def config(self):
        return self.automator.config

    @property
    def test_session(self):
        return self.automator.test_session

    @property
    def context(self):
        return self.automator.context

    @property
    def label(self):
        return self.__label

    @property
    def def_file_name(self):
        return self.__def_file_name

    @property
    def def_file_path(self):
        return self.__def_file_path

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def qual_name(self):
        return self.__class__.__qualname__

    @property
    def parent(self):
        return self.__parent

    def __check_reg_status(self):
        if self.__gui_registered:
            raise Exception("Attempt to change Gui critical attribute post registration with Setu.")

    def is_gui(self):
        return True

    def set_label(self, label):
        self.__check_reg_status()
        self.__label = label

    def set_def_file_name(self, name):
        self.__check_reg_status()
        self.__def_file_name = name

    def _register(self):
        if self.__gui_registered:
            raise Exception("Attempt to re-register Gui with Setu.")

        if not self.__parent:
            self.__impl_gui = self.test_session.define_gui(self.automator, label=self.label, name=self.name, qual_name=self.qual_name, def_file_path=self.def_file_path)
        else:
            self.__impl_gui = self.__parent.impl_gui.define_gui(self.automator, label=self.label, name=self.name, qual_name=self.qual_name, def_file_path=self.def_file_path)

        if self.__parent:
            self.__parent.add_child(self.__label, self)

        self.__load()

    def add_child(self, label, gui):
        self.__children_map[label.lower()] = gui

    def get_child(self, label):
        if label:
            if label.lower() in self.__children_map:
                return self.__children_map[label.lower()]
            else:
                raise Exception("No child Gui with label: {} defined.".format(label))
        else:
            raise Exception("Child Gui label is None.")

    def reach_until(self):
        # Children can override and write any necessary loading instructions
        pass

    def validate_readiness(self):
        pass

    def __load(self):
        try:
            self.validate_readiness()
        except:
            try:
                self.reach_until()
                self.validate_readiness()
            except Exception as e:
                raise Exception(
                    "UI [{}] with SetuId [{}] did not load as expected. Error: {}.",
                    self.__class__.__name__,
                    self.get_setu_id(),
                    str(e)
                )

    def element(self, *str_or_with_locators):
        gom_element = self.impl_gui.define_element(*str_or_with_locators)
        return GuiAutoComponentFactory.Element(self.automator, gom_element)

    def multi_element(self, *str_or_with_locators):
        return self.impl_gui.define_multi_element(*str_or_with_locators)

    def dropdown(self, *str_or_with_locators):
        return self.impl_gui.define_dropdown(*str_or_with_locators)

    def radio_group(self, *str_or_with_locators):
        return self.impl_gui.define_radio_group(*str_or_with_locators)

    def tab_group(self, *str_or_with_locators, tab_header_locator, content_relation_attr, content_relation_type):
        impl = self.impl_gui.define_tabgroup(
            *str_or_with_locators,
            tab_header_locator=tab_header_locator, 
            content_relation_attr=content_relation_attr, 
            content_relation_type=content_relation_type
        )
        return GuiAutoComponentFactory.TabGroup(self.automator, gom_element)

    def alert(self, *str_or_with_locators):
        return self.impl_gui.define_alert(*str_or_with_locators)

    def frame(self, *str_or_with_locators):
        return self.impl_gui.define_frame(*str_or_with_locators)

    def child_window(self, *str_or_with_locators):
        return self.impl_gui.define_child_window(*str_or_with_locators)

    @property
    def main_window(self):
        return self.impl_gui.define_main_window()

    @property
    def dom_root(self):
        return self.impl_gui.dom_root

    @property
    def browser(self):
        return self.impl_gui.browser