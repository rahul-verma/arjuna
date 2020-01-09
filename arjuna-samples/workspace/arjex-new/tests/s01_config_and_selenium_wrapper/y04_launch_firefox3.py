
from arjuna.revised.tpi import Arjuna

'''
Code is same as that for launching Chrome.
To launch Firefox instead, you need to add the following to <arjex/config/project.conf file:
arjunaOptions = {
    browser.name = firefox
}
'''

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



