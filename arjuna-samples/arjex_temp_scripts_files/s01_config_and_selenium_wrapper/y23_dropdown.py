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
Testers use 3 approaches for Dropdown controls in web test automation using Selenium.
1. Using Selenium's Select class as it provides higher level methods.
2. Using sendKeys() method of WebElement.
3. (Especially for custom select controls) - Click the drop down control and then click the option. 

Arjuna tries to cater to all of them with a single abstraction - its DropDown object.

3 will be covered later when element configuration has been discussed.
'''

from commons import *
from arjuna import *

init_arjuna()
wordpress = login()

wordpress.ui.element(With.link_text("Settings")).click()

role_select = wordpress.ui.dropdown(With.id("default_role"))
role_select.select_value("editor")

role_select.select_text("Subscriber")
print(role_select.has_visible_text_selected("Subscriber"))
print(role_select.has_value_selected("subscriber"))
print(role_select.has_index_selected(2))
print(role_select.value)
print(role_select.text)

role_select.select_index(4)
print(role_select.has_index_selected(4))

text = "Subscriber"

role_select.text = text
assert role_select.has_visible_text_selected("Subscriber") is True

logout(wordpress)