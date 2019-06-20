from arjuna.client.core.action import SetuActionType
from arjuna.client.core.connector import SetuArg
from .automator import AbstractAppAutomator

from arjuna.tpi.guiauto import With


class BaseGui(AbstractAppAutomator):

    def __init__(self, automator, label=None, def_file_name=None, parent=None, register=True):
        super().__init__(automator.get_config())

        self.__automator = automator
        self.__children_map = dict()
        self.__auto_context = automator.get_automation_context()
        self.__test_session = automator.get_test_session()
        self._set_automator_setu_id_arg(automator.get_setu_id())
        self.__gui_registered = False
        self.__parent = parent

        self.__label = None
        self.__def_file_name = None

        if label:
            self.set_label(label)

        if def_file_name:
            self.set_def_file_name(def_file_name)

        if register:
            self._register()

    def __check_reg_status(self):
        if self.__gui_registered:
            raise Exception("Attempt to change Gui critical attribute post registration with Setu.")

    def is_gui(self):
        return True

    def set_label(self, label):
        self.__check_reg_status()
        self.__label = label
        self.set_def_file_name(label + ".gns")

    def set_def_file_name(self, name):
        self.__check_reg_status()
        self.__def_file_name = name

    def _register(self):
        if self.__gui_registered:
            raise Exception("Attempt to re-register Gui with Setu.")

        args = [
            SetuArg.arg("testSessionSetuId", self.__test_session.get_setu_id()),
            SetuArg.arg("automatorSetuId", self.__automator.get_setu_id()),
            SetuArg.arg("label", self.__label),
            SetuArg.arg("name", self.__class__.__name__),
            SetuArg.arg("qualName", self.__class__.__qualname__),
            SetuArg.arg("defFileName", self.__def_file_name)
        ]

        gui_setu_id = None
        if not self.__parent:
            gui_setu_id = self.__test_session.create_gui(self.__automator, *args)
        else:
            args.append(SetuArg.arg("parentGuiSetuId", self.__parent.get_setu_id()))
            response = self._send_request(SetuActionType.GUIAUTO_GUI_CREATE_GUI, *args)
            gui_setu_id = response.get_gui_setu_id()

        self._set_setu_id(gui_setu_id)
        self._set_self_setu_id_arg("guiSetuId")

        if self.__parent:
            self.__parent.add_child(self.__label, self)

        self.__load()

    def _get_automator(self):
        return self.__automator

    def get_qualified_name(self):
        return self.__class__.__qualname__

    def add_child(self, label, gui):
        self.__children_map[label.lower()] = gui

    def get_child(self, label):
        if label:
            if label.lower() in self.__children_map:
                return self.__children_map[label.lower()]
            else:
                raise Exception("No child Gui with label: {} defined.".format(label))
        else:
            raise Exception("Child Gui label is None.")

    def reach_until(self):
        # Children can override and write any necessary loading instructions
        pass

    def validate_readiness(self):
        pass

    def __load(self):
        try:
            self.validate_readiness()
        except:
            try:
                self.reach_until()
                self.validate_readiness()
            except Exception as e:
                raise Exception(
                    "UI [{}] with SetuId [{}] did not load as expected. Error: {}.",
                    self.__class__.__name__,
                    self.get_setu_id(),
                    str(e)
                )

    def __convert_with(self, input):
        if isinstance(input, With):
            return input
        else:
            return With.assigned_name(input)

    def Element(self, name_or_with_obj):
        return super().Element(self.__convert_with(name_or_with_obj))

    def MultiElement(self, name_or_with_obj):
        return super().MultiElement(self.__convert_with(name_or_with_obj))

    def DropDown(self, name_or_with_obj):
        return super().DropDown(self.__convert_with(name_or_with_obj))

    def RadioGroup(self, name_or_with_obj):
        return super().RadioGroup(self.__convert_with(name_or_with_obj))

    def Alert(self, name_or_with_obj):
        return super().Alert(self.__convert_with(name_or_with_obj))

    def Frame(self, name_or_with_obj):
        return super().Frame(self.__convert_with(name_or_with_obj))

    def ChildWindow(self, name_or_with_obj):
        return super().ChildWindow(self.__convert_with(name_or_with_obj))

    def MainWindow(self):
        return self.get_automator().MainWindow()

    def DomRoot(self):
        return self.get_automator().DomRoot()

    def Browser(self):
        return self.get_automator().Browser()

    def get_automator(self):
        return self.__automator