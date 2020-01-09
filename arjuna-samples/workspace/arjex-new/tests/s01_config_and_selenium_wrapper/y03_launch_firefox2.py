
from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.enums import BrowserName, ArjunaOption

context = Arjuna.init()
cb = context.config_builder
cb.firefox()
cb.build()

# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(context.get_config())

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



