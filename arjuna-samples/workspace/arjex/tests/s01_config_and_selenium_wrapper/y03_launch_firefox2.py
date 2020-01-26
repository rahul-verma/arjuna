from commons import *
from arjuna.tpi.enums import BrowserName, ArjunaOption
from arjuna.tpi.guiauto import WebApp

context = init_arjuna()
cc = context.config_creator
cc.firefox()
cc.register()

google = WebApp(base_url="https://google.com", config=context.get_config())
google.launch()
print(google.ui.main_window.title)
google.quit()


