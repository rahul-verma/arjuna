from commons import *
from arjuna import *

init_arjuna()
wordpress = login()

main_win = wordpress.ui.main_window
main_win.maximize()
print(main_win.title)

wordpress.ui.execute_javascript("window.open('/abc')")
cwin = wordpress.ui.latest_child_window
cwin.focus()
print(cwin.title)
cwin.close()

wordpress.ui.execute_javascript("window.open('https://rahulverma.net')")
wordpress.ui.execute_javascript("window.open('https://google.com')")
wordpress.ui.close_all_child_windows()
print(main_win.title)

wordpress.ui.execute_javascript("window.open('https://rahulverma.net')")
wordpress.ui.execute_javascript("window.open('https://google.com')")

dwin = wordpress.ui.child_window(With.window_title("Google"))
dwin.focus()
dwin.title
dwin.close()

wordpress.ui.execute_javascript("window.open('https://rahulverma.net')")
wordpress.ui.execute_javascript("window.open('https://google.com')")

dwin = wordpress.ui.child_window(With.window_ptitle("gle"))
dwin.focus()
dwin.title
dwin.close()

wordpress.ui.execute_javascript("window.open('https://rahulverma.net')")
wordpress.ui.execute_javascript("window.open('https://google.com')")

dwin = wordpress.ui.child_window(With.content_locator(With.value("Google Search")))
dwin.focus()
dwin.title
dwin.close()

logout(wordpress)