from arjuna.lib.setu.core.requester.config import SetuArg, SetuActionType
from arjuna.tpi.guiauto import With
from .automator import AbstractAppAutomator


class BaseGui(AbstractAppAutomator):

    def __init__(self, automator, label=None, def_file_name=None, parent=None):
        super().__init__(automator.getConfig())

        self.__automator = automator
        self.__children_map = dict()
        self.__auto_context = automator.getAutomationContext()
        self.__test_session = automator.getTestSession()
        self._set_automator_setu_id_arg(automator.getSetuId())
        self.__gui_registered = False
        self.__parent = parent

        self.__label = None
        self.__def_file_name = None

        if label:
            self.setLabel(label)

        if def_file_name:
            self.setDefFileName(def_file_name)

    def __check_reg_status(self):
        if self.__gui_registered:
            raise Exception("Attempt to change Gui critical attribute post registration with Setu.")

    def is_gui(self):
        return True

    def set_label(self, label):
        self.__check_reg_status()
        self.label = label
        self.setDefFileName(label + ".gns")

    def set_def_file_name(self, name):
        self.__check_reg_status()
        self.__def_file_name = name

    def register_with_setu(self):
        if self.__gui_registered:
            raise Exception("Attempt to re-register Gui with Setu.")

        args = [
            SetuArg.arg("testSessionSetuId", self.testSession.getSetuId()),
            SetuArg.arg("automatorSetuId", self.__automator.getSetuId()),
            SetuArg.arg("label", self.__label),
            SetuArg.arg("name", self.__class__.__name__),
            SetuArg.arg("qualName", self.__class__.__qualname__),
            SetuArg.arg("defFileName", self.__def_file_name)
        ]

        gui_setu_id  = None
        if not self.__parent:
            gui_setu_id = self.testSession.createGui(self.__automator, *args)
        else:
            args.append(SetuArg.arg("parentGuiSetuId", self.__parent.getSetuId()))
            response = self._send_request(SetuActionType.GUIAUTO_GUI_CREATE_GUI, *args)
            gui_setu_id = response.getGuiSetuId()


        self.setSetuId(gui_setu_id)
        self.setSelfSetuIdArg("guiSetuId")

        if self.__parent:
            self.__parent.addChild(self.__label, self)

        self.__load()

    def _get_automator(self):
        return self.__automator

    def get_qualified_name(self):
        return self.__class__.__qualname__

    def add_child(self, label, gui):
        self.__children_map[label.lower()] = gui

    def ChildGui(self, label):
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

    def elememt(self, name):
        return self.element(With.assignedName(name))

    def multiElement(self, name):
        return self.multiElement(With.assignedName(name))

    def dropdown(self, name):
        return self.dropdown(With.assignedName(name))

    def radioGroup(self, name):
        return self.dropdown(With.assignedName(name))

    def alert(self, name):
        return self.dropdown(With.assignedName(name))

    def frame(self, name):
        return self.dropdown(With.assignedName(name))

    def childWindow(self, name):
        return self.dropdown(With.assignedName(name))

    def mainWindow(self):
        return self.automator.mainWindow()

    def domRoot(self):
        return self.automator.domRoot()

    def browser(self):
        return self.automator.browser()

    def automator(self):
        return self.__automator