import os
from arjuna.interact.gui.gom.impl.base import BaseGui
from arjuna.tpi.enums import ArjunaOption

class DefaultGui(BaseGui):
    '''
        This class provides a means for direct creation of Gui objects without inheritance.
    '''

    def __init__(self, automator, ns_dir, def_file_name, parent=None):
        super().__init__(automator, ns_dir=ns_dir, def_file_name=def_file_name, parent=parent)


class SimpleBaseGui(BaseGui):
    '''
        This class is meant to be inherited from, so that you can implement a more involed GOM model.
    '''

    def __init__(self, automator, ns_dir):
        super().__init__(automator, ns_dir=ns_dir)

class SimpleBaseWidget(BaseGui):

    def __init__(self, automator, parent, ns_dir):
        super().__init__(automator, parent=parent, ns_dir=ns_dir)
        label = self.__class__.__name__