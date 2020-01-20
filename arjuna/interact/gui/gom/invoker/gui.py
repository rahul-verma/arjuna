import os
from .base import BaseGui
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

class SimpleBaseChildGui(BaseGui):

    def __init__(self, automator, parent, app_def_dir=""):
        super().__init__(automator, parent=parent, register=False)
        label = self.__class__.__name__
        self.set_label(label)
        self.set_def_file_name("{}/{}.gns".format(app_def_dir, label))
        self._register()