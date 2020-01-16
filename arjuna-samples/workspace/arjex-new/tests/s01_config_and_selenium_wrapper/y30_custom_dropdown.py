'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''

from arjuna.revised.tpi import Arjuna
from arjuna.revised.tpi.guiauto.helpers import With
from arjuna.revised.tpi.guiauto.helpers import Screen

from .wp_login_logout import *

Arjuna.init()
# Default Gui automation engine is Selenium
automator = Arjuna.create_gui_automator(Arjuna.get_central_config())

url = automator.config.get_user_option_value("narada.ex.dropdown.url").as_str()
automator.browser.go_to_url(url)

conf = GuiActionConfig.builder().check_type(False).check_post_state(False).build()

dropdown = automator.element(With.id("DropDown").configure(config))
dropdown.set_option_container(With.class_name("dropdown"))
dropdown.set_option_locators(With.class_name("dropdown-item"))
dropdown.select_index(2)

automator.quit()