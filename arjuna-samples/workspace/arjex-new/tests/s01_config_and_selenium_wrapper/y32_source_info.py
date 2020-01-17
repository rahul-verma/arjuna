from arjuna.tpi import Arjuna
from arjuna.tpi.guiauto.helpers import With, GuiActionConfig

from commons import *

def print_source_info(source):
    print(source.content.root)
    print(source.content.all)
    print(source.content.inner)
    print(source.content.text)	

init_arjuna()
automator = launch_automator()
go_to_wp_home(automator)


element = automator.element(With.id("loginform"))
print_source_info(element.source)

login(automator, at_home=False)

automator.element(With.link_text("Settings")).click()

# Dopdown
element = automator.dropdown(With.id("default_role"))
print_source_info(element.source)

# Radio
date_format = automator.radio_group(With.name("date_format"))
print_source_info(date_format.source)


# Automator source
automator.element(With.link_text("Posts")).click()
automator.element(With.link_text("Add New")).click()
print_source_info(automator.source)

print_source_info(automator.dom_root.source)

frame = automator.frame(With.id("content_ifr"))
frame.focus()
print_source_info(frame.source)

# custom drop down
url = automator.config.get_user_option_value("narada.ex.dropdown.url").as_str()
automator.browser.go_to_url(url)

conf = GuiActionConfig.builder().check_type(False).check_post_state(False).build()

dropdown = automator.dropdown(
    With.id("DropDown"),
    option_container_locators=With.class_name("dropdown"),
    option_locators=With.class_name("dropdown-item")
)
    
dropdown.configure(conf)
print_source_info(dropdown.source)

logout(automator)