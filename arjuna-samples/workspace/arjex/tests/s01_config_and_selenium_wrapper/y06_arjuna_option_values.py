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

from commons import *
from arjuna import *

init_arjuna()
config = Arjuna.get_ref_config()

wait_time = config.guiauto_max_wait_time
print(wait_time)

wait_value = config.get_arjuna_option_value(ArjunaOption.GUIAUTO_MAX_WAIT)
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("GUIAUTO_MAX_WAIT")
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("GuIAuTo_MaX_WaIt")
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("guiauto.max.wait")
print(wait_value.as_int())

wait_value = config.get_arjuna_option_value("guiauto.max.wait")
print(wait_value.as_int())

should_maximize_browser = config.get_arjuna_option_value(ArjunaOption.BROWSER_MAXIMIZE)
print(should_maximize_browser.as_bool())
