'''
Code is same as that for launching Chrome.
To launch Firefox instead, you need to add the following to <arjex/config/project.conf file:
arjunaOptions = {
    browser.name = firefox
}
'''
from commons import *
from arjuna import *

init_arjuna()
google = WebApp(base_url="https://google.com")
google.launch()
print(google.ui.main_window.title)
google.quit()

