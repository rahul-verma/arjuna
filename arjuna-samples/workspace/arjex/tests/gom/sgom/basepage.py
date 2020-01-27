import unittest
from arjuna.interact.gui.gom import Page

class WPBasePage(Page):

    def __init__(self, app, automator):
        super().__init__(app=app, automator=automator)
        self.externalize_guidef()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()
        from sgom.home import HomePage
        return HomePage(self.app, self.automator)


