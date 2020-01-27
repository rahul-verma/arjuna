from commons import *
from arjuna import *

context = init_arjuna()
eb = GuiDriverExtendedConfigBuilder()
eb.browser_arg("--headless")
econfig = eb.build()

google = WebApp(base_url="https://google.com", ext_config=econfig)
google.launch()
print(google.ui.main_window.title)
google.quit()



