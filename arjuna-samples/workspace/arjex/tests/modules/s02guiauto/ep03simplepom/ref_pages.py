from arjuna.tpi.guiauto import SimpleBaseGui


class WPBasePage(SimpleBaseGui):

    def __init__(self, automator):
        super().__init__(automator, "wordpress")

    def logout(self):
        self.Browser().go_to_url(self.get_automator().get_config().get_user_option_value("wp.logout.url").as_string())