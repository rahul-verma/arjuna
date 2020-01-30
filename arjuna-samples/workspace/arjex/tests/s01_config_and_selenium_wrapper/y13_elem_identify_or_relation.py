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

from arjuna import *
from commons import *

init_arjuna()
wordpress = create_wordpress_app()

# Two identifiers. Only first one would be tried as it succeeds.
element = wordpress.ui.element(With.id("user_login"), With.name("log"))
print(element.source.content.root)

# Two identifiers. First invalid, second valid. Hence it succeeds by using second With construct
# Identification max wait time is for all With constructs clubbed together.
element = wordpress.ui.element(With.id("INVALID"), With.name("d"))
print(element.source.content.root)

wordpress.quit()