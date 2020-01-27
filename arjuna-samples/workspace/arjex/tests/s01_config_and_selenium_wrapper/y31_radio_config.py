from commons import *
from arjuna.interact.gui.helpers import With, GuiActionConfig

init_arjuna()

automator = launch_automator()

url = automator.config.get_user_option_value("narada.ex.radio.url").as_str()
automator.browser.go_to_url(url)

radios = automator.radio_group(With.name("Traditional"))
radios.select_index(1)

# Tag mix up
radios = automator.radio_group(With.name("Prob1"))
radios.select_index(1)

# Type mix up
radios = automator.radio_group(With.name("Prob2"))
radios.select_index(1)

# Group mix up
radios = automator.radio_group(With.class_name("Prob3"))
radios.select_index(1)

# state check off
conf = GuiActionConfig.builder().check_pre_state(False).build()
radios = automator.element(With.name("Traditional").configure(config))
radios.select_index(1)

# tag mix up, state check off
conf = GuiActionConfig.builder().check_pre_state(False).build()
radios = automator.element(With.name("Prob1").configure(config))
radios.select_index(1)

automator.quit()