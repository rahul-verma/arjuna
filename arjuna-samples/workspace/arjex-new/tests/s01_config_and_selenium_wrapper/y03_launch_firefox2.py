from commons import *

context = init_arjuna()
cb = context.ConfigBuilder()
cb.firefox()
cb.build()

# Default Gui automation engine is Selenium
automator = launch_automator(context.get_config())

automator.browser.go_to_url("https://google.com")
print(automator.main_window.title)
automator.quit()



