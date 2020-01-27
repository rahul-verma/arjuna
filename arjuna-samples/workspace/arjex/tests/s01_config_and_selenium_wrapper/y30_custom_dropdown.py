'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''

from commons import *
from arjuna.interact.gui.helpers import With, GuiActionConfig

init_arjuna()

automator = launch_automator()

url = automator.config.get_user_option_value("narada.ex.dropdown.url").as_str()
automator.browser.go_to_url(url)

conf = GuiActionConfig.builder().check_type(False).check_post_state(False).build()

dropdown = automator.dropdown(
                    With.id("DropDown"), 
                    option_container_locators = With.class_name("dropdown"),
                    option_locators = With.class_name("dropdown-item")
                )
dropdown.configure(conf)
dropdown.select_index(2)

# automator.quit()