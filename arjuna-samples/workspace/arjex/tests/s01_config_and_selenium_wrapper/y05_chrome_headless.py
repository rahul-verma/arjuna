from commons import *
from arjuna.tpi.enums import BrowserName, ArjunaOption
from arjuna.tpi.guiauto import WebApp
from arjuna.tpi.guiauto.helpers import GuiDriverExtendedConfigBuilder

context = init_arjuna()
eb = GuiDriverExtendedConfigBuilder()
eb.browser_arg("--headless")
econfig = eb.build()

google = WebApp(base_url="https://google.com", ext_config=econfig)
google.launch()
print(google.ui.main_window.title)
google.quit()



