from enum import Enum, auto
from .basepage import WPFullPage

class SettingsPage(WPFullPage):

    class loc(Enum):
        role = auto()

    def tweak_settings(self):
        role_select = self.dropdown(self.loc.role)
        role_select.select_value("editor")
        self._asserter.assertEqual("editor", role_select.value, "Author type selection failed.")
        return self
