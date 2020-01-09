from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

login(automator)

main_win = automator.main_window
main_win.maximize()
print(main_win.title)

automator.execute_script("window.open('/abc')")
cwin = automator.get_latest_window()
cwin.focus()
print(cwin.get_title())
cwin.close()

automator.execute_script("https://rahulverma.net")
automator.execute_script("https://google.com")
automator.close_all_child_windows()
print(main_win.title)

logout(automator)