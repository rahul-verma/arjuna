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
wordpress = login()

main_win = wordpress.ui.main_window
main_win.maximize()
print(main_win.title)

wordpress.ui.execute_javascript("window.open('/abc')")
cwin = wordpress.ui.latest_child_window
cwin.focus()
print(cwin.title)
cwin.close()

wordpress.ui.execute_javascript("window.open('https://rahulverma.net')")
wordpress.ui.execute_javascript("window.open('https://google.com')")
wordpress.ui.close_all_child_windows()
print(main_win.title)

logout(wordpress)