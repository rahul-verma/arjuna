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

go_to_wp_home(automator)

'''
The following code is for user name field.
Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">

Params: 
APP URL: E.g. http://192.168.56.103
Page: E.g. wp-login
Resulting in http://192.168.56.103/wp-login.php
'''

identifier = r"//*[@action='$app_url$/$page$.php']"

String app_url = automator.config.getUserOptionValue("wp.app.url").as_str();
String page = "wp-login"

# Positional
GuiElement element = automator.Element(With.xpath(identifier).format(appURL, page))
element.identify()
print(element.source.content.root)

# Named
element = automator.Element(With.xpath(identifier).format(app_url=app_url, page=page))
element.identify()
print(element.source.content.root)


# Named params need not be passed in order, providing you flexibility, readability and preventing positional errors.
element = automator.Element(With.xpath(identifier).format(page=page, app_url=app_url))
element.identify()
print(element.source.content.root)

# Names for parameters are case-insensitive
element = automator.Element(With.xpath(identifier).format(PaGe=page, aPP_Url=app_url))
element.identify()
print(element.source.content.root)

logout(automator)