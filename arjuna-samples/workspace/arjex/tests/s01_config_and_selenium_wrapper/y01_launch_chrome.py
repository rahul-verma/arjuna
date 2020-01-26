from commons import *

from arjuna.tpi.guiauto import WebApp

init_arjuna()
google = WebApp(base_url="https://google.com")
google.launch()
print(google.ui.main_window.title)
google.quit()



