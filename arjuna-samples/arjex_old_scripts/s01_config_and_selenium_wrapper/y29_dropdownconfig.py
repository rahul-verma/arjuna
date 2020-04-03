# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
3. (Especially for custom select controls) - Click the drop down control and then click the option. 
'''

from commons import *
from arjuna import *

init_arjuna()

narada = create_app()

url = narada.ui.config.user_options.value("narada.ex.dropdown.url")
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