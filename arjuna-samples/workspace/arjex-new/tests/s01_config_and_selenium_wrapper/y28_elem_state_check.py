'''
Testers use 3 approaches for Dropdown controls in web test automation using Selenium.
1. Using Selenium's Select class as it provides higher level methods.
2. Using sendKeys() method of WebElement.
3. (Especially for custom select controls) - Click the drop down control and then click the option. 

Arjuna tries to cater to all of them with a single abstraction - its DropDown object.

3 will be covered later when element configuration has been discussed.
'''

from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("narada.ex.elemstate.url").as_str()
automator.browser.go_to_url(url)

automator.element(With.id("target")).click()
automator.alert.confirm()

automator.browser.go_to_url(url)
conf = GuiActionConfig.builder().check_pre_state(False).build()

automator.element(With.id("target")).configure(conf).click()
automator.alert.confirm()