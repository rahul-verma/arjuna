from arjuna.tpi.enums import ArjunaOption

from .guiautomator import GuiAutomator
from .handler import Handler
from enum import Enum, auto

class MobileView(Enum):
    NATIVE_APP = auto()
    WEBVIEW = auto()


class ViewContextHandler(Handler):

    def __init__(self, automator: GuiAutomator):
        super().__init__(automator)

    def switch_to_view_context(self, view_name):
        self._act(TestAutomatorActionBodyCreator.switch_to_view_context(view_name))

    def get_current_view_context(self):
        response = self._act(TestAutomatorActionBodyCreator.get_current_view_context())
        return response["data"]["viewContext"]

    def get_all_view_contexts(self):
        response = self._act(TestAutomatorActionBodyCreator.get_all_view_contexts())
        return response["data"]["viewContexts"]

    def switch_to_native_view(self):
        self.switch_to_view_context(MobileView.NATIVE_APP.name)

    def switch_to_web_view(self, pkg):
        self.switch_to_view_context(
            "{}_{}".format(MobileView.WEBVIEW.name, pkg)
        )

    def switch_to_first_web_view(self):
        for context_name in self.get_all_view_contexts():
            if context_name.find(MobileView.WEBVIEW.name) != -1:
                self.switch_to_view_context(context_name)
                break

    def _does_name_represent_web_view(self, view_name):
        return view_name.lower().find(MobileView.WEBVIEW.name.lower()) != -1 

    def is_web_view(self):
        return self._does_name_represent_web_view(self.get_current_view_context())

    def is_native_view(self):
        return self.get_current_view_context().lower() == MobileView.WEBVIEW.name.lower()