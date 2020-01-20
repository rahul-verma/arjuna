from arjuna.tpi.guiauto.helpers import _WithType
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

    def __lmd(self, *locators):
        out = []
        for locator in locators:
            if locator.wtype == _WithType.GNS_NAME:
                out.extend(self.gui_def.convert_to_with(locator))
            else:
                out.append(locator)
        return out

    def define_element(self, *with_locators):
        return self.automator.element(*self.__lmd(*with_locators))

    def define_multielement(self, *with_locators):
        return self.automator.multielement(*self.__lmd(*with_locators))

    def define_dropdown(self, *with_locators):
        return self.automator.dropdown(*self.__lmd(*with_locators))

    def define_radiogroup(self, *with_locators):
        return self.automator.radiogroup(*self.__lmd(*with_locators))

    def define_frame(self, *with_locators):
        return self.automator.frame(*self.__lmd(*with_locators))

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