import uuid
from arjuna.interact.gui.gom.impl.namestore import GuiNameStore
from arjuna.interact.gui.gom.impl.gui import Gui
from arjuna.interact.gui.gom.impl.guidef import GuiDef
from arjuna.tpi.enums import ArjunaOption

class GuiManager:

    def __init__(self, project_config):
        self.__name_store = GuiNameStore()
        self.__namespace_dir = project_config.arjuna_config.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)

    @property
    def name_store(self):
        return self.__name_store

    @property
    def namespace_dir(self):
        return self.__namespace_dir

    def define_gui(self, automator, label=None, name=None, qual_name=None, def_file_path=None):
        gui_def = GuiDef(self.__name_store, self.__namespace_dir, automator, label, def_file_path)
        gui = Gui(self, automator, gui_def)
        return gui


