from arjuna.tpi import Arjuna
from arjuna.interact.gui.helpers import With

from commons import *

init_arjuna()
automator = launch_automator()
login(automator)

main_win = automator.main_window
main_win.maximize()
print(main_win.title)

automator.execute_javascript("window.open('/abc')")
cwin = automator.latest_child_window
cwin.focus()
print(cwin.title)
cwin.close()

automator.execute_javascript("window.open('https://rahulverma.net')")
automator.execute_javascript("window.open('https://google.com')")
automator.close_all_child_windows()
print(main_win.title)

logout(automator)