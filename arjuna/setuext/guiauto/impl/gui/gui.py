import os

from arjuna.tpi.enums import ArjunaOption
from .nsloader import GuiNamespaceLoaderFactory
from arjuna.setu.types import SetuConfiguredObject
from arjuna.setuext.guiauto.impl.locator.emd import SimpleGuiElementMetaData, GuiElementMetaData, Locator


class Gui(SetuConfiguredObject):

    def __init__(self, name_store, namespace_dir, automator, label, file_def_path):
        super().__init__(automator.config)
        self.__name_store = name_store
        self.__namespace_dir = namespace_dir
        self.__automator = automator
        self.__auto_context = self.config.setu_config.get_guiauto_context()
        self.__file_def_path = os.path.abspath(os.path.join(self.__namespace_dir, file_def_path.strip()))
        self.__ns = None
        ns_name = "file_ns::" + self.__file_def_path.lower()
        if name_store.has_namespace(ns_name):
            self.__ns = name_store.get_namespace(ns_name)
        else:
            self.__ns = name_store.load_namespace(
                ns_name, 
                GuiNamespaceLoaderFactory.create_namespace_loader(self.__file_def_path)
        )

        self.__children = []

    def add_child(self, label, automator, file_def_path):
        self.__children.append(
            Gui(self.__name_store, self.__namespace_dir, label, self.__automator, file_def_path)
    )

    def get_emd(self, locators):
        final_locators = []
        for raw_locator in locators:
            if raw_locator["withType"].upper().strip() == "ASSIGNED_NAME":
                emd = self.__ns.get_meta_data(raw_locator["withValue"], self.__auto_context)
                final_locators.extend(emd.raw_locators)
            else:
                final_locators.append(Locator(ltype=raw_locator["withType"], lvalue=raw_locator["withValue"]))
        return GuiElementMetaData(final_locators)

    def create_dispatcher(self):
        # Pages don't use any dispatcher
        pass

class GuiFactory:

    @classmethod
    def create_app_from_dir(cls, name, automator, app_def_dir):
        considered_path = app_def_dir
        if not os.path.isdir(considered_path):
            ns_dir = automator.config.value(ArjunaOption.GUIAUTO_NAMESPACE_DIR)
            full_path = os.path.join(ns_dir, considered_path)
            considered_path = os.path.abspath(full_path)
            if not os.path.isdir(considered_path):
                raise Exception("Provided root definition path is not a directory: {}".format(app_def_dir))

        app = Gui(automator, os.path.join(considered_path, "HomePage.gns"), label=name)
        children_dir = os.path.join(considered_path, "children")
        if os.path.isdir(children_dir):
            lfiles = os.listdir(children_dir)
            for f in lfiles:
                cpath = os.path.join(children_dir, f)
                if os.path.isfile(cpath):
                    base_name = os.path.basename(cpath)
                    app.add_child(base_name, cpath)

    @classmethod
    def create_gui(cls, automator, def_path):
        return Gui(automator, def_path)