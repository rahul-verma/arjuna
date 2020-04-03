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

from commons import *
from arjuna import *

init_arjuna()

narada = create_app()

url = narada.config.user_options.value("narada.ex.radio.url")
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