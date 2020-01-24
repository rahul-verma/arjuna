from enum import Enum
from arjuna.tpi.guiauto.helpers import With, WithType
from arjuna.interact.gui.auto.invoker.component import GuiAutoComponentFactory
from arjuna.interact.gui.auto.impl.locator.emd import GuiElementMetaData
from .guidef import GuiDef

class Gui:

    def __init__(self, gui_mgr, automator, gui_def, parent=None):
        self.__guimgr = gui_mgr
        self.__guidef = gui_def
        self.__automator = automator
        self.__parent = parent

    @property
    def gui_def(self):
        return self.__guidef

    @property
    def automator(self):
        return self.__automator

    def define_gui(self, automator, label=None, name=None, qual_name=None, def_file_path=None):
        gui_def = GuiDef(self.__guimgr.name_store, self.__guimgr.namespace_dir, automator, label, def_file_path)
        gui = Gui(self, automator, gui_def, parent=self)
        return gui

    def convert_to_with_lmd(self, *raw_str_or_with_locators):
        out = []
        for locator in raw_str_or_with_locators:
            w = None
            if isinstance(locator, With):
                w = locator
            elif type(locator) is str:
                w = With.gns_name(locator)
            elif isinstance(locator, Enum):
                w = With.gns_name(locator.name)
            else:
                raise Exception("A With object or name of element is expected as argument.")

            if w.wtype == WithType.GNS_NAME:
                out.extend(self.gui_def.convert_to_with(w))
            else:
                out.append(w)
        return GuiElementMetaData.create_lmd(*out)

    def define_element(self, *str_or_with_locators):
        return GOMElement(self, self.automator.impl_automator.define_element(self.convert_to_with_lmd(*str_or_with_locators)))

    def define_multielement(self, *str_or_with_locators):
        return self.automator.multielement(self.convert_to_with_lmd(*str_or_with_locators))

    def define_dropdown(self, *str_or_with_locators):
        return self.automator.dropdown(self.convert_to_with_lmd(*str_or_with_locators))

    def define_radiogroup(self, *str_or_with_locators):
        return self.automator.radiogroup(self.convert_to_with_lmd(*str_or_with_locators))

    def define_tabgroup(self, *str_or_with_locators, tab_header_locator, content_relation_attr, content_relation_type):
        return self.automator.impl_automator.define_tabgroup(
            self.convert_to_with_lmd(*str_or_with_locators),
            tab_header_lmd=self.convert_to_with_lmd(tab_header_locator),
            content_relation_attr=content_relation_attr, 
            content_relation_type=content_relation_type
        )

    def define_frame(self, *str_or_with_locators):
        return self.automator.frame(self.convert_to_with_lmd(*str_or_with_locators))

    @property
    def alert(self):
        return self.automator.alert

    @property
    def main_window(self):
        return self.automator.main_window

    @property
    def browser(self):
        return self.automator.browser

    def set_slomo(self, on, interval=None):
        self.automator.set_slomo(on, interval)


class GOMElement:

    def __init__(self, gui, impl, index=None):
        self.__index = index
        self.impl_gui = gui
        self.impl = impl

    @property
    def source(self):
        return self.impl.get_source()

    @property
    def text(self):
        return self.source.get_text_content()

    @text.setter
    def text(self, text):
        self.impl.set_text(text)

    def click(self):
        self.impl.click()

    def wait_until_present(self):
        self.impl.wait_until_present()

    def wait_until_visible(self):
        self.impl.wait_until_visible()

    def wait_until_clickable(self):
        self.impl.wait_until_clickable()

    def check(self):
        self.impl.check()

    def uncheck(self):
        self.impl.uncheck()

    def identify(self):
        self.impl.identify()

    def hover(self):
        self.impl.hover()

    def element(self, *with_locators):
        gom_element = self.impl.define_element(self.impl_gui.convert_to_with_lmd(*with_locators))
        return GuiAutoComponentFactory.Element(self, gom_element)

    def multi_element(self, *with_locators):
        return self.impl.define_multielement(self.impl_gui.convert_to_with_lmd(*with_locators))