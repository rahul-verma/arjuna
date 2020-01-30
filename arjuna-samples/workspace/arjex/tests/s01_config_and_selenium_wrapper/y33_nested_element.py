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

# Locate the form and then all input elements
form = wordpress.ui.element(With.id("loginform"))
user_box = form.element(With.tag_name("input"))
print(user_box.source.content.all)
labels = form.multi_element(With.tag_name("label"))
for label in labels:
    print(label.text)
    print(label.source.content.all)
    i = label.element(With.tag_name("input"))
    print(i.source.content.all)

wordpress.quit()