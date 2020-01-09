
from arjuna.revised.tpi import Arjuna

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



