from commons import *

'''
Code is same as that for launching Chrome.
To launch Firefox instead, you need to add the following to <arjex/config/project.conf file:
arjunaOptions = {
    browser.name = firefox
}
'''

init_arjuna()
# Default Gui automation engine is Selenium
automator = launch_automator(Arjuna.get_ref_config())

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



