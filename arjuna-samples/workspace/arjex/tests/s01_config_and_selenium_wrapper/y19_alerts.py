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
wordpress = login()

wordpress.ui.execute_javascript("alert('dummy')")
wordpress.ui.alert.confirm()
wordpress.ui.execute_javascript("alert('dummy')")
wordpress.ui.alert.dismiss()

wordpress.ui.execute_javascript("alert('dummy')")
alert = wordpress.ui.alert
assert alert.text == "dummy"
alert.confirm()

wordpress.ui.execute_javascript("prompt('Are You Sure?')")
alert = wordpress.ui.alert
alert.text = "Yes"
alert.confirm()

logout(wordpress)