import sys
from pprint import pprint
from commons import *
from arjuna.tpi.enums import BrowserName, ArjunaOption

context = init_arjuna()
cb = context.ConfigBuilder()
cb.arjuna_option(ArjunaOption.BROWSER_NAME, BrowserName.FIREFOX)
cb.build()

automator = launch_automator(context.get_config())

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



