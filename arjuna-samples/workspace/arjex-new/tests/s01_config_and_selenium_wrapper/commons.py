from arjuna.tpi import Arjuna
from arjuna.tpi.guiauto.helpers import With

def init_arjuna():
    from arjuna.tpi import Arjuna
    return Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex-new")

def launch_automator(config=None, econfig=None):
    # Default Gui automation engine is Selenium
    config = config and config or Arjuna.get_ref_config()
    return Arjuna.create_gui_automator(config=config, extended_config=econfig)

def go_to_wp_home(automator):
    url = automator.config.get_user_option_value("wp.login.url").as_str()
    automator.browser.go_to_url(url)

def login(automator):
    go_to_wp_home(automator)

    user, pwd = automator.config.get_user_option_value("wp.users.admin").split_as_str_list()

    # Login
    automator.element(With.id("user_login")).set_text(user)
    automator.element(With.id("user_pass")).set_text(pwd)
    automator.element(With.id("wp-submit")).click()

    automator.element(With.class_name("welcome-view-site")).wait_until_visible()

def logout(automator):
    url = automator.config.get_user_option_value("wp.logout.url").as_str()
    automator.browser.go_to_url(url)

    automator.element(With.link_ptext("log out")).click()
    message = automator.element(With.ptext("logged out")).wait_until_visible()

    automator.quit()
