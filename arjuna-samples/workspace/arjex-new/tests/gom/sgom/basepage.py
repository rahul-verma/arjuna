import unittest
from arjuna.interact.gui.gom.invoker.gui import SimpleBaseGui

class WPBasePage(SimpleBaseGui):

    def __init__(self, automator):
        super().__init__(automator, "wordpress")
        # Trick to use assertions outside of a unittest test
        self._asserter = unittest.TestCase('__init__')

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()