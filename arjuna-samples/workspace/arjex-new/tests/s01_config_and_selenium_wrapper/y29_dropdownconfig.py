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

dropdown = automator.Element(With.id("DropDown"))
dropdown.select_visible_text("Another option")

# Wrong Tag
dropdown = automator.Element(With.id("Prob1"))
dropdown.select_index(1)

#State check off
conf = GuiActionConfig.builder().check_pre_state(False).build()
dropdown = automator.Element(With.id("test").configure(config))
dropdown.select_index(1)

# Wrong tag, state check off
conf = GuiActionConfig.builder().check_pre_state(False).build()
dropdown = automator.Element(With.id("Prob1").configure(config))
dropdown.select_index(1)

automator.quit()