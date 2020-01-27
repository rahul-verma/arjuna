import uuid
from arjuna.interact.gui.gom.namestore import GuiNameStore
from arjuna.core.enums import ArjunaOption

class GuiManager:

    def __init__(self, config):
        self.__name_store = GuiNameStore()
        self.__namespace_dir = config.arjuna_config.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)

    @property
    def name_store(self):
        return self.__name_store

    @property
    def namespace_dir(self):
        return self.__namespace_dir

    def define_gui(self, automator, label=None, name=None, qual_name=None, def_file_path=None):
        from arjuna.interact.gui.gom.guidef import GuiDef
        gui_def = GuiDef(self.__name_store, self.__namespace_dir, automator, label, def_file_path)
        gui = Gui(self, automator, gui_def)
        return gui


