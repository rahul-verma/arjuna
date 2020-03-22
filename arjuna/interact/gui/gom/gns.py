
from .formatter import GNSFormatter

class GNS:

    def __init__(self, container, gui_def):
        self.__container = container
        self.__gui_def = gui_def

    def format(self, **kwargs):
        return GNSFormatter(self, self.__gui_def, **kwargs)

    def locate_with_emd(self, emd):
        from arjuna.interact.gui.gom.gui import Gui
        if isinstance(self.__container, Gui):
            if not self.__container.root_element:
                return getattr(self.__container, "_" + emd.meta.template.name.lower())(emd)
            else:
                return getattr(self.__container.root_element, "_" + emd.meta.template.name.lower())(self.__container, emd)
        else:
            return getattr(self.__container, "_" + emd.meta.template.name.lower())(self.__container.gui, emd)

    def __getattr__(self, name):
        emd = self.__gui_def.get_emd(name)
        fmt_emd = emd.create_formatted_emd() # Only globals will be processed.
        from arjuna import log_debug
        log_debug("Finding element with label: {} and emd: {}".format(name, fmt_emd))
        return self.locate_with_emd(fmt_emd)
