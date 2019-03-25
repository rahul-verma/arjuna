from arjuna.tpi import Arjuna

config = Arjuna.init()

automator = Arjuna.createGuiAutomator(config)

automator.browser().goToUrl("https://www.google.com")
print(automator.mainWindow().getTitle())
automator.quit()