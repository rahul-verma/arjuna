from .basepage import WPBasePage
from .dashboard import DashboardPage

class HomePage(WPBasePage):

    def login(self, user, pwd):
        self.element("login").text = user
        self.element("password").text = pwd
        self.element("submit").click()

        self.element("view_site").wait_until_visible()
        return DashboardPage(self)

    def login_with_default_creds(self):
        user, pwd = self.config.get_user_option_value("wp.users.admin").split_as_str_list()
        return self.login(user, pwd)