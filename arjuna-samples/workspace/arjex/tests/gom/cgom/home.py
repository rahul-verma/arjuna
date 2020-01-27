from enum import Enum, auto
from .basepage import WPBasePage
from .dashboard import DashboardPage

class HomePage(WPBasePage):

    class loc(Enum):
        login = auto()
        password = auto()
        submit = auto()
        view_site = auto()

    def login(self, user, pwd):
        self.element(self.loc.login).text = user
        self.element(self.loc.password).text = pwd
        self.element(self.loc.submit).click()

        self.element(self.loc.view_site).wait_until_visible()
        return DashboardPage(self)

    def login_with_default_creds(self):
        user, pwd = self.config.get_user_option_value("wp.users.admin").split_as_str_list()
        return self.login(user, pwd)
