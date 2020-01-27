import unittest
from arjuna import Page

class WPBasePage(Page):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.externalize_guidef()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()
        from sgom.home import HomePage
        return HomePage(self)


