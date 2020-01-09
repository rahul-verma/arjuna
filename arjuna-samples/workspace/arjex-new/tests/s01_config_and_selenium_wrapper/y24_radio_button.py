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

login(automator)

automator.Element(With.link_text("Settings")).click()

date_format = automator.RadioGroup(With.name("date_format"))
System.out.println(date_format.has_value_selected("Y-m-d"))
System.out.println(date_format.has_index_selected(1))
System.out.println(date_format.get_first_selected_option_value())
date_format.select_value(r"\c\u\s\t\o\m")
date_format.select_index(2)

logout(automator)