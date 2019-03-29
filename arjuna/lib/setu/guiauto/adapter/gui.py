import uuid
from arjuna.lib.setu.guiauto.lib.gui.namestore import GuiNameStore
from arjuna.lib.setu.guiauto.lib.gui.gui import Gui
from arjuna.tpi.enums import ArjunaOption


class GuiHandlerManager:

    def __init__(self, project_config):
        self.__name_store = GuiNameStore()
        self.__namespace_dir = project_config.setu_config.value(ArjunaOption.GUI_NAMESPACE_DIR)
        self.__gui_map = {}

    def create_gui(self, automator_handler, json_dict):
        label = json_dict["label"]
        defPath = json_dict["defFileName"]
        gui = Gui(self.__name_store, self.__namespace_dir, automator_handler.automator, label, defPath)
        gui_handler = GuiHandler(automator_handler, gui)
        self.__gui_map[gui.setu_id] = gui_handler
        return gui_handler

    def get_gui_handler(self, setu_id):
        return self.__gui_map[setu_id]


# Arg names of methods show JSON names, so don't follow Python conventions.
class GuiHandler:

    def __init__(self, automator_handler, gui):
        self.__gui = gui
        self.__automator_handler = automator_handler
        self.__automator = None

    @property
    def gui(self):
        return self.__gui

    @property
    def setu_id(self):
        return self.__gui.setu_id

    @property
    def automator_handler(self):
        return self.__automator_handler

    def create_element(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.create_element_with_emd(emd)

    def create_multielement(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.create_multielement_with_emd(emd)

    def create_dropdown(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.create_dropdown_with_emd(emd)

    def create_radiogroup(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.create_radiogroup_with_emd(emd)

    def create_frame(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.create_frame_with_emd(emd)

    def create_alert(self):
        return self.automator_handler.create_alert()

    def get_main_window(self):
        return self.automator_handler.get_main_window()

    def set_slomo(self, on, interval=None):
        self.automator_handler.set_slomo(on, interval)

    def take_window_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_window_action(action, elem_setu_id, json_dict)

    def take_main_window_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_main_window_action(action, elem_setu_id, json_dict)

    def take_child_window_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_child_window_action(action, elem_setu_id, json_dict)

    def take_browser_action(self, action, json_dict):
        return self.automator_handler.take_browser_action(action, json_dict)

    def take_element_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_element_action(action, elem_setu_id, json_dict)

    def take_multielement_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_multielement_action(action, elem_setu_id, json_dict)

    def take_dropdown_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_dropdown_action(action, elem_setu_id, json_dict)

    def take_radiogroup_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_radiogroup_action(action, elem_setu_id, json_dict)

    def take_alert_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_alert_action(action, elem_setu_id, json_dict)

    def take_domroot_action(self, action, json_dict):
        return self.automator_handler.take_domroot_action(action, json_dict)

    def take_frame_action(self, action, elem_setu_id, json_dict):
        return self.automator_handler.take_frame_action(action, json_dict)