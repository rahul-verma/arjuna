'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''

from commons import *
from arjuna.interact.gui.helpers import With, GuiActionConfig

init_arjuna()

automator = launch_automator()

url = automator.config.get_user_option_value("narada.ex.dropdown.url").as_str()
automator.browser.go_to_url(url)

# # Works. Waits for clickability of select control as well as option.
# dropdown = automator.dropdown(With.id("test"))
# dropdown.select_visible_text("Another Option")

# # Wrong Tag
# dropdown = automator.dropdown(With.id("Prob1"))
# dropdown.select_index(1)

# # State check off
# conf = GuiActionConfig.builder().check_pre_state(False).build()
# dropdown = automator.dropdown(With.id("test")).configure(conf)
# dropdown.select_index(1)

# # Wrong tag, state check off
# conf = GuiActionConfig.builder().check_pre_state(False).build()
# dropdown = automator.dropdown(With.id("Prob1")).configure(conf)
# dropdown.select_index(1)

# automator.quit()