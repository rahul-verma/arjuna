from enum import Enum, auto
from .basepage import WPFullPage

class DashboardPage(WPFullPage):

    class loc(Enum):
        settings = auto()

    def go_to_settings(self):
        self.element(self.loc.settings).click()
        return SettingsPage(self)