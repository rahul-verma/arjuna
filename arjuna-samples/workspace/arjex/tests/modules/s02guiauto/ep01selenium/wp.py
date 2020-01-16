from arjuna.tpi.guiauto import With


class WPLoginLogout:

    @staticmethod
    def login(automator):
        automator.Browser().go_to_url(automator.get_config().get_user_option_value("wp.login.url").as_string())
        automator.element(With.id("user_login")).set_text("user")
        automator.element(With.id("user_pass")).set_text("bitnami")
        automator.element(With.id("wp-submit")).click()
        automator.element(With.class_name("welcome-view-site")).wait_until_clickable()

    @staticmethod
    def logout(automator):
        automator.Browser().go_to_url(automator.get_config().get_user_option_value("wp.logout.url").as_string())
        automator.quit()