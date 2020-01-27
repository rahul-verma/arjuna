from .basepage import WPFullPage

class SettingsPage(WPFullPage):

    def tweak_settings(self):
        role_select = self.dropdown("role")
        role_select.select_value("editor")
        self._asserter.assertEqual("editor", role_select.value, "Author type selection failed.")
        return self
