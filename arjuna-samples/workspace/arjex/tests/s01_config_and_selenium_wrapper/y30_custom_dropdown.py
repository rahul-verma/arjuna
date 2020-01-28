'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''


from commons import *
from arjuna import *

init_arjuna()

narada = create_app()

url = narada.config.get_user_option_value("narada.ex.dropdown.url").as_str()
narada.ui.browser.go_to_url(url)

conf = GuiInteractionConfig.builder().check_type(False).check_post_state(False).build()

dropdown = narada.ui.dropdown(
                    With.id("DropDown"), 
                    option_container_locator = With.class_name("dropdown"),
                    option_locator = With.class_name("dropdown-item"),
                    iconfig=conf
                )
dropdown.select_index(2)

narada.quit()