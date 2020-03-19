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

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="ArjunaExtended")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def check_arjuna_exts(request, wordpress):

    # Based on partial text
    wordpress.element(text="Lost")

    # Based on Full Text
    wordpress.element(ftext="Lost your password?")

    # Based on Title
    wordpress.element(title="Password Lost and Found")

    # Based on Value
    wordpress.element(value="Log In")

    # Based on partial match of content of an attribute
    wordpress.element(attr=Attr("for", "_login"))

    # Based on full match of an attribute
    wordpress.element(fattr=Attr("for", "user_login"))

    # Based on element type
    wordpress.element(type="password")

    # Based on compound classes
    wordpress.element(classes="button button-large")
    wordpress.element(classes=("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    wordpress.element(point=Point(1043, 458))

    # With Javascript
    wordpress.element(js="return document.getElementById('wp-submit')")