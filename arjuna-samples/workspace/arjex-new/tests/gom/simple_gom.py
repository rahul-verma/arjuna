import unittest

from base import BaseTest
from sgom.home import HomePage

class WPBaseTest(BaseTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboard_page = None

    def setUp(self):
        super().setUp()
        self.dashboard_page = HomePage(self.automator).login_with_default_creds()

    def tearDown(self):
        self.dashboard_page.logout()
        # self.automator.quit()

class SimplePOMTest(WPBaseTest):

    def test_author_type_selection(self):
        self.dashboard_page.go_to_settings().tweak_settings()
        self.assertEqual("editor", role_select.first_selected_option_value, "Author type selection failed.")

unittest.main()