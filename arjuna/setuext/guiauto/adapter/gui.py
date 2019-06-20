import uuid
from arjuna.setuext.guiauto.impl.gui.namestore import GuiNameStore
from arjuna.setuext.guiauto.impl.gui.gui import Gui
from arjuna.tpi.enums import ArjunaOption
from arjuna.client.core.action import *
from .action_map import *
from arjuna.setu.adapter import Handler

class GuiHandlerManager:

    def __init__(self, project_config):
        self.__name_store = GuiNameStore()
        self.__namespace_dir = project_config.setu_config.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)
        self.__gui_map = {}

    @property
    def name_store(self):
        return self.__name_store

    @property
    def namespace_dir(self):
        return self.__namespace_dir

    def add_to_gui_map(self, setu_id, gui_handler):
        self.__gui_map[setu_id] = gui_handler

    def take_action(self, automator_handler, action_type, json_args):
        if action_type == GuiActionType.CREATE_GUI:
            gui_handler = self.create_gui(automator_handler, json_args)
            return {"guiSetuId" : gui_handler.setu_id}
        elif action_type == GuiActionType.CREATE_CHILD_GUI:
            return self.create_child_gui(automator_handler, json_args)
        else:
            raise Exception("Unknown action got for Gui Mananger: " + action_type.name)

    def create_gui(self, automator_handler, json_args):
        label = json_args["label"]
        defPath = json_args["defFileName"]
        gui = Gui(self.__name_store, self.__namespace_dir, automator_handler.automator, label, defPath)
        gui_handler = GuiHandler(self, automator_handler, gui)
        self.add_to_gui_map(gui.setu_id, gui_handler)
        return gui_handler

    def create_child_gui(self, automator_handler, json_args):
        parent_gui_setu_id = json_args.pop("parentGuiSetuId")
        parent_gui_handler = self.get_gui_handler(parent_gui_setu_id)
        return parent_gui_handler.create_gui(automator_handler, **json_args)

    def get_gui_handler(self, setu_id):
        return self.__gui_map[setu_id]


# Arg names of methods show JSON names, so don't follow Python conventions.
class GuiHandler:

    def __init__(self, gui_mgr, automator_handler, gui):
        self.__guimgr = gui_mgr
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

    def create_gui(self, automator_handler, label=None, name=None, qualName=None, defFileName=None):
        gui = Gui(self.__guimgr.name_store, self.__guimgr.namespace_dir, automator_handler.automator, label, defFileName)
        gui_handler = GuiHandler(self.__guimgr, automator_handler, gui)
        self.__guimgr.add_to_gui_map(gui.setu_id, gui_handler)
        return {"guiSetuId": gui.setu_id}

    def take_action(self, action_type, json_args):
        action_id = HANDLER_MAP[action_type]
        method_name, replaceable = HANDLER_NAME_MAP[action_id]
        return getattr(self, method_name)(action_type.name.replace(replaceable, "").lower(), json_args)

    def take_direct_action(self, action, json_args):
        Handler._pop_arg(json_args, "automatorSetuId")
        return getattr(self, action)(**json_args)

    def define_element(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.define_element_with_emd(emd)

    def define_multielement(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.define_multielement_with_emd(emd)

    def define_dropdown(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.define_dropdown_with_emd(emd)

    def define_radiogroup(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.define_radiogroup_with_emd(emd)

    def define_frame(self, locators):
        emd = self.gui.get_emd(locators)
        return self.automator_handler.define_frame_with_emd(emd)

    def define_alert(self):
        return self.automator_handler.define_alert()

    def define_main_window(self):
        return self.automator_handler.get_main_window()

    def set_slomo(self, on, interval=None):
        self.automator_handler.set_slomo(on, interval)

    def take_window_action(self, action, json_dict):
        return self.automator_handler.take_window_action(action, json_dict)

    def take_main_window_action(self, action, json_dict):
        return self.automator_handler.take_main_window_action(action, json_dict)

    def take_child_window_action(self, action, json_dict):
        return self.automator_handler.take_child_window_action(action, json_dict)

    def take_browser_action(self, action, json_dict):
        return self.automator_handler.take_browser_action(action, json_dict)

    def take_element_action(self, action, json_dict):
        return self.automator_handler.take_element_action(action, json_dict)

    def take_multielement_action(self, action, json_dict):
        return self.automator_handler.take_multielement_action(action, json_dict)

    def take_dropdown_action(self, action, json_dict):
        return self.automator_handler.take_dropdown_action(action, json_dict)

    def take_radiogroup_action(self, action, json_dict):
        return self.automator_handler.take_radiogroup_action(action, json_dict)

    def take_alert_action(self, action, json_dict):
        return self.automator_handler.take_alert_action(action, json_dict)

    def take_domroot_action(self, action, json_dict):
        return self.automator_handler.take_domroot_action(action, json_dict)

    def take_frame_action(self, action, json_dict):
        return self.automator_handler.take_frame_action(action, json_dict)