import unittest

from base import BaseTest
from cgom import basepage, widgets
from cgom.home import HomePage

class WPBaseTest(BaseTest):

    def __init__(self, *args, **kwargs):
        basepage.GNS_FMT = "MGNS"
        widgets.GNS_FMT = "MGNS"
        super().__init__(*args, **kwargs)
        self.dashboard_page = None

    def setUp(self):
        super().setUp()
        self.dashboard_page = HomePage(self.automator).login_with_default_creds()

    def tearDown(self):
        self.dashboard_page.top_nav.logout()
        # self.automator.quit()

class CompositeGOMTest(WPBaseTest):

    def test_author_type_selection(self):
        self.dashboard_page.left_nav.settings.tweak_settings()

unittest.main()