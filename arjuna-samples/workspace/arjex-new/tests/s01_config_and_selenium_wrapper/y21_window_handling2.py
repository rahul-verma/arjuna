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

automator.execute_javascript("window.open('/abc')")
cwin = automator.get_latest_window()
cwin.focus()
print(cwin.get_title())
cwin.close()

automator.execute_javascript("https://rahulverma.net")
automator.execute_javascript("https://google.com")
automator.close_all_child_windows()
print(main_win.title)

automator.execute_javascript("https://rahulverma.net")
automator.execute_javascript("https://google.com")

dwin = automator.Window(With.window_title("abc"))
dwin.focus()
dwin.title
dwin.close()

automator.execute_javascript("https://rahulverma.net")
automator.execute_javascript("https://google.com")

dwin = automator.Window(With.partial_window_title("abc"))
dwin.focus()
dwin.title
dwin.close()

automator.execute_javascript("https://rahulverma.net")
automator.execute_javascript("https://google.com")

dwin = automator.Window(With.element(With.value("Google Search")))
dwin.focus()
dwin.title
dwin.close()

logout(automator)