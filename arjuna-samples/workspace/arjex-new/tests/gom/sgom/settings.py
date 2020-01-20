from .basepage import WPBasePage

class SettingsPage(WPBasePage):

    def tweak_settings(self):
        role_select = self.dropdown("role")
        role_select.select_value("editor")
        self._asserter.assertEqual("edidtor", role_select.first_selected_option_value, "Author type selection failed.")
        return self
