from arjuna import *

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

automator.execute_javascript("window.open('https://rahulverma.net')")
automator.execute_javascript("window.open('https://google.com')")

dwin = automator.child_window(With.window_title("Google"))
dwin.focus()
dwin.title
dwin.close()

automator.execute_javascript("window.open('https://rahulverma.net')")
automator.execute_javascript("window.open('https://google.com')")

dwin = automator.child_window(With.window_ptitle("gle"))
dwin.focus()
dwin.title
dwin.close()

automator.execute_javascript("window.open('https://rahulverma.net')")
automator.execute_javascript("window.open('https://google.com')")

dwin = automator.child_window(With.content_locator(With.value("Google Search")))
dwin.focus()
dwin.title
dwin.close()

logout(automator)