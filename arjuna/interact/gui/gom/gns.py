
class GNS:

    def __init__(self, container, gui_def):
        self.__container = container
        self.__gui_def = gui_def

    def __getattr__(self, name):
        emd = self.__gui_def.get_emd(name)
        from arjuna import Arjuna
        Arjuna.get_logger().debug("Finding element with label: {} and emd: {}".format(name, emd))
        from arjuna.interact.gui.gom.gui import Gui
        if isinstance(self.__container, Gui):
            if not self.__container.root_element:
                return getattr(self.__container, emd.meta.template.name.lower())(emd)
            else:
                return getattr(self.__container.root_element, emd.meta.template.name.lower())(self.__container, emd)
        else:
            return getattr(self.__container, emd.meta.template.name.lower())(self.__container.gui, emd)
