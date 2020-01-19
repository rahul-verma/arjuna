import unittest
import time

from arjuna.tpi.guiauto.helpers import With
from arjuna.interact.gui.gom.invoker.gui import DefaultGui

from base import BaseTest

class WPBaseTest(BaseTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        super().setUp()
        self.app = DefaultGui(self.automator, "WordPress", "simpleapp/WordPress.gns")
        self.login_with_default_creds()

    def tearDown(self):
        self.logout()
        #self.app.automator.quit()

    def login_with_default_creds(self):
        self.app.browser.go_to_url(self.config.get_user_option_value("wp.login.url").as_str())

        user, pwd = self.config.get_user_option_value("wp.users.admin").split_as_str_list()

        # Login
        self.app.element("login").set_text(user)
        self.app.element("password").set_text(pwd)
        self.app.element("submit").click()

        self.app.element("view-site").wait_until_visible()

    def logout(self):
        print("print LOGout")
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.app.browser.go_to_url(url)

        self.app.element("logout_confirm").click()
        self.app.element("logout_msg").wait_until_visible()

class SimpleAppTest(WPBaseTest):

    def test_author_type_selection(self):
        self.app.element("Settings").click()

        role_select = self.app.dropdown("role")
        role_select.select_value("editor")

        self.assertEqual("editor", role_select.first_selected_option_value, "Author type selection failed.")

unittest.main()