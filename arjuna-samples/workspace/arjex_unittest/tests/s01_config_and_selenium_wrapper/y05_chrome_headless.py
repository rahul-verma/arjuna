
from commons import *
from arjuna.tpi.guiauto.helpers import GuiDriverExtendedConfigBuilder

init_arjuna()
eb = GuiDriverExtendedConfigBuilder()
eb.browser_arg("--headless")
econfig = eb.build()

# Default Gui automation engine is Selenium
automator = launch_automator(Arjuna.get_ref_config(), econfig)

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



