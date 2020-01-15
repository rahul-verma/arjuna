from commons import *

init_arjuna()
automator = launch_automator()
automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



