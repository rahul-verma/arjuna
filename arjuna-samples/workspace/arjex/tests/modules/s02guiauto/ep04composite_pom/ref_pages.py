from arjuna.tpi.guiauto import SimpleBaseGui, SimpleBaseChildGui


class WPBasePage(SimpleBaseGui):

    def __init__(self, automator):
        super().__init__(automator, "wordpress")


class WPChildPage(SimpleBaseChildGui):

    def __init__(self, automator, parent):
        super().__init__(automator, parent, "wordpress")


class TopMenuBar(WPChildPage):

    def __init__(self, automator, parent):
        super().__init__(automator, parent)

    def logout(self):
        self.Browser().go_to_url(self.get_automator().get_config().get_user_option_value("wp.logout.url").as_string())


class LeftNavSideBar(WPChildPage):

    def __init__(self, automator, parent):
        super().__init__(automator, parent)

    def go_to_settings(self):
        from .app_pages import SettingsPage
        self.Element("settings").click()
        return SettingsPage(self.get_automator())


class WPFullPage(WPBasePage):

    def __init__(self, automator):
        super().__init__(automator)
        self.__top_nav = TopMenuBar(automator, self)
        self.__lef_nav = LeftNavSideBar(automator, self)

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__lef_nav

