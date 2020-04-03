
from .formatter import GNSFormatter
from arjuna.tpi.exceptions import *
from arjuna.interact.gui.auto.finder import GuiEmdFinder, GuiElementEmdFinder

class GNS:

    def __init__(self, gui_or_element, gui_def):
        self.__container_type = None
        self.__gui = None
        self.__container = None
        self.__process_container(gui_or_element)
        self.__gui_def = gui_def
        if self.__container_type == "gui":
            self.__finder = GuiEmdFinder(self.__gui)
        else:
            self.__finder = GuiElementEmdFinder(self.__container)

    def __process_container(self, gui_or_element):
        from .gui import Gui
        if isinstance(gui_or_element, Gui):
            if not gui_or_element.root_element:
                self.__container_type = "gui"
                self.__container = gui_or_element
                self.__gui = gui_or_element
            else:
                self.__container_type = "element"
                self.__container = gui_or_element.root_element
                self.__gui = gui_or_element
        else:
            self.__container_type = "element"
            self.__container = gui_or_element 
            self.__gui = gui_or_element.gui  
        self.__loaded = True         

    def format(self, **kwargs):
        return GNSFormatter(self, self.__gui_def, **kwargs)

    def __get_emd_for_label(self, label):
        emd = self.__gui_def.get_emd(label)
        return emd.create_formatted_emd() # Only globals will be processed.

    def wait_until_absent(self, *labels):
        waiter = getattr(self.__container, "_" + "wait_until_absent")
        for label in labels:
            emd = self.__get_emd_for_label(label)
            try:
                waiter(emd)
            except GuiElementPresentError:
                raise GuiElementForLabelPresentError(self.__gui, label)    

    def contains(self, *labels):
        for label in labels:
            try:
                getattr(self, label)
            except GuiElementForLabelNotPresentError:
                continue
            else:
                return True
        return False

    def locate_with_emd(self, emd):
        factory = getattr(self.__finder, emd.meta["template"].name.lower())
        return factory(emd)
        

    def __getattr__(self, label):
        emd = self.__get_emd_for_label(label)
        from arjuna import log_debug
        log_debug("Finding element with label: {} and emd: {}".format(label, emd))
        try:
            return self.locate_with_emd(emd)
        except ArjunaTimeoutError:
            raise GuiElementForLabelNotPresentError(self.__gui, label)
