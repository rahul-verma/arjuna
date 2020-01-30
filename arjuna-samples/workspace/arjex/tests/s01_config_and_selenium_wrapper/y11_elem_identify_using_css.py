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
wordpress = create_wordpress_app()

# Based on any attribute e.g. for
element = wordpress.ui.element(With.css_selector("*[for = 'user_login']"))
print(element.source.content.root)

# Based on partial content of an attribute
element = wordpress.ui.element(With.css_selector("*[for *= '_login']"))
print(element.source.content.root)

# Based on element type
element = wordpress.ui.element(With.css_selector("*[type ='password']"))
print(element.source.content.root)

# Based on compound classes
element = wordpress.ui.element(With.css_selector(".button.button-large"))
print(element.source.content.root)

wordpress.quit()