from .base import BaseGui

class DefaultGui(BaseGui):

    def __init__(self, automator, label, def_file_name, parent=None):
        super().__init__(automator, label=label, def_file_name=def_file_name, parent=parent)


class SimpleBaseGui(BaseGui):

    def __init__(self, automator, app_def_dir=""):
        super().__init__(automator, register=False)
        label = self.__class__.__name__
        self.set_label(label)
        self.set_def_file_name("{}/{}.gns".format(app_def_dir, label))
        self._register()


class SimpleBaseChildGui(BaseGui):

    def __init__(self, automator, parent, app_def_dir=""):
        super().__init__(automator, parent=parent, register=False)
        label = self.__class__.__name__
        self.set_label(label)
        self.set_def_file_name("{}/{}.gns".format(app_def_dir, label))
        self._register()