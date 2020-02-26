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

'''
The following code is for user name field.
Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">

Params: 
APP URL: E.g. http://192.168.56.103
Page: E.g. wp-login
Resulting in http://192.168.56.103/wp-login.php
'''

identifier = r"//*[@action='$app_url$/$page$.php']"

app_url = wordpress.ui.config.get_user_option_value("wp.app.url")
page = "wp-login"

element = wordpress.ui.element(With.xpath(identifier).format(app_url=app_url, page=page))
print(element.source.content.root)


# Named params need not be passed in order, providing you flexibility, readability and preventing positional errors.
element = wordpress.ui.element(With.xpath(identifier).format(page=page, app_url=app_url))
print(element.source.content.root)

# Names for parameters are case-insensitive
element = wordpress.ui.element(With.xpath(identifier).format(PaGe=page, aPP_Url=app_url))
print(element.source.content.root)

logout(wordpress)