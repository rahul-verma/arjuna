'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''


from commons import *
from arjuna import *

init_arjuna()

narada = create_app()

url = narada.config.user_options.value("narada.ex.dropdown.url")
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