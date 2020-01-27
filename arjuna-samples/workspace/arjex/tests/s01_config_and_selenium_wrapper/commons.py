from arjuna import *

def init_arjuna():
    return Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex")

def create_app():
    app = WebApp()
    app.launch(blank_slate=True)
    return app
    
def create_wordpress_app():
    url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=url)
    wordpress.launch()
    return wordpress

def login():
    wordpress = create_wordpress_app()

    user, pwd = wordpress.config.get_user_option_value("wp.users.admin").split_as_str_list()

    # Login
    wordpress.ui.element(With.id("user_login")).text = user
    wordpress.ui.element(With.id("user_pass")).text = pwd
    wordpress.ui.element(With.id("wp-submit")).click()

    wordpress.ui.element(With.class_name("welcome-view-site")).wait_until_visible()
    return wordpress

def logout(wordpress):
    url = wordpress.config.get_user_option_value("wp.logout.url").as_str()
    wordpress.ui.browser.go_to_url(url)

    wordpress.ui.element(With.link_ptext("log out")).click()
    message = wordpress.ui.element(With.ptext("logged out")).wait_until_visible()

    wordpress.quit()
