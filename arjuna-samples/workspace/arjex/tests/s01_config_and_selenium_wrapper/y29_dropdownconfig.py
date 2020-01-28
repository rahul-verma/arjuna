'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''

from commons import *
from arjuna import *

init_arjuna()

narada = create_app()

url = narada.ui.config.get_user_option_value("narada.ex.dropdown.url").as_str()
narada.ui.browser.go_to_url(url)

# # Works. Waits for clickability of select control as well as option.
# dropdown = narada.ui.dropdown(With.id("test"))
# dropdown.select_text("Another Option")

# # Wrong Tag
# narada.ui.dropdown(With.id("Prob1")).select_index(1)

# State check off
# conf = GuiInteractionConfig.builder().check_pre_state(False).build()
# narada.ui.dropdown(With.id("test"), iconfig=conf).select_index(1)

# # # Wrong tag, state check off
# conf = GuiInteractionConfig.builder().check_pre_state(False).build()
# narada.ui.dropdown(With.id("Prob1"), iconfig=conf).select_index(1)

narada.quit()