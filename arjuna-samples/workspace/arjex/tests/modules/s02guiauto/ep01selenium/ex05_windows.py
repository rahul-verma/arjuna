from arjuna.tpi import Arjuna
from arjuna.tpi.markup import *

from .wp import WPLoginLogout


@test_function
def test(my):
    automator = Arjuna.create_gui_automator()

    WPLoginLogout.login(automator)

    main_win = automator.MainWindow()
    main_win.maximize()
    print(main_win.get_title())

    automator.execute_javascript("window.open('/abc')")
    win = automator.LatestChildWindow()
    win.focus()
    print(win.get_title())
    win.close()

    automator.execute_javascript("window.open('/def')")
    automator.execute_javascript("window.open('/xyz')")
    automator.close_all_child_windows()
    print(main_win.get_title())
    
    WPLoginLogout.logout(automator)
