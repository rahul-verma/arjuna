from commons import *
from arjuna import *

init_arjuna()
google = WebApp(base_url="https://google.com")
google.launch()
print(google.ui.main_window.title)
google.quit()



