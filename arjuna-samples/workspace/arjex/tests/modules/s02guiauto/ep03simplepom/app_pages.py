from .ref_pages import WPBasePage


class HomePage(WPBasePage):

    def __init__(self, automator):
        super().__init__(automator)

    def login(self):
        self.Browser().go_to_url(self.get_automator().get_config().get_user_option_value("wp.login.url").as_string())
        self.Element("login").set_text("user")
        self.Element("password").set_text("bitnami")
        self.Element("submit").click()
        self.Element("view-site").wait_until_clickable()
        return DashboardPage(self.get_automator())

class DashboardPage(WPBasePage):

    def __init__(self, automator):
        super().__init__(automator)

    def go_to_settings(self):
        self.Element("settings").click()
        return SettingsPage(self.get_automator())


class SettingsPage(WPBasePage):

    def __init__(self, automator):
        super().__init__(automator)

    def tweak_settings(self):
        role_select = self.DropDown("role")
        print(role_select.has_visible_text_selected("Subscriber"))
        print(role_select.has_value_selected("subscriber"))
        print(role_select.has_index_selected(2))
        print(role_select.get_first_selected_option_text())
        role_select.select_by_value("editor")
        role_select.select_by_visible_text("Subscriber")
        role_select.select_by_index(4)
        return self
