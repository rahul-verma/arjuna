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

def print_source_info(src):
    print(source.content.root)
    print(source.content.all
    print(source.content.inner)
    print(source.content.text)	   

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

go_to_wp_home(automator)


element = automator.Element(With.id("loginform"))
print_source_info(element.source)

login(automator)

automator.Element(With.link_text("Settings")).click()

# Dopdown
element = automator.DropDown(With.id("default_role"))
print_source_info(element.source)

# Radio
date_format = automator.RadioGroup(With.name("date_format"))
print_source_info(date_format.source)


# Automator source
automator.Element(With.link_text("Posts")).click()
automator.Element(With.link_text("Add New")).click()
print_source_info(automator.source)

print_source_info(automator.dom_root.source)

automator.Frame(With.id("content_ifr")).focus()
print_source_info(frame.source)

# custom drop down
url = automator.config.get_user_option_value("narada.ex.dropdown.url").as_str()
automator.browser.go_to_url(url)

conf = GuiActionConfig.builder().check_type(False).check_post_state(False).build()

dropdown = automator.Element(With.id("DropDown").configure(config))
dropdown.set_option_container(With.class_name("dropdown"))
dropdown.set_option_locators(With.class_name("dropdown-item"))
print_source_info(dropdown.source)

logout(automator)