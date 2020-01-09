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

url = automator.config.get_user_option_value("narada.ex.radio.url").as_str()
automator.browser.go_to_url(url)

radios = automator.RadioGroup(With.name("Traditional"))
radios.select_index(1)

# Tag mix up
radios = automator.RadioGroup(With.name("Prob1"))
radios.select_index(1)

# Type mix up
radios = automator.RadioGroup(With.name("Prob2"))
radios.select_index(1)

# Group mix up
radios = automator.RadioGroup(With.class_name("Prob3"))
radios.select_index(1)

# state check off
conf = GuiActionConfig.builder().check_pre_state(False).build()
radios = automator.Element(With.name("Traditional").configure(config))
radios.select_index(1)

# tag mix up, state check off
conf = GuiActionConfig.builder().check_pre_state(False).build()
radios = automator.Element(With.name("Prob1").configure(config))
radios.select_index(1)

automator.quit()