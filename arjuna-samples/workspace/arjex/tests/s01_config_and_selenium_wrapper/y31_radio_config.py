from commons import *
from arjuna import *

init_arjuna()

narada = create_app()

url = narada.config.get_user_option_value("narada.ex.radio.url").as_str()
narada.ui.browser.go_to_url(url)

narada.ui.radio_group(With.name("Traditional")).select_index(1)

# Tag mix up
narada.ui.radio_group(With.name("Prob1")).select_index(1)

# Type mix up
narada.ui.radio_group(With.name("Prob2")).select_index(1)

# Group mix up
radios = narada.ui.radio_group(With.class_name("Prob3"))
radios.select_index(1)

# state check off
conf = GuiInteractionConfig.builder().check_pre_state(False).build()
narada.ui.element(With.name("Traditional", iconfig=conf).select_index(1)

# tag mix up, state check off
conf = GuiInteractionConfig.builder().check_pre_state(False).build()
narada.ui.element(With.name("Prob1", iconfig=conf).select_index(1)

narada.quit()