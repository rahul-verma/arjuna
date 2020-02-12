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

'''
Code is kept redundant across methods for the purpose of easier learning.
'''

@test
def test_basic_identifiers(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()

    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    element = wordpress.ui.element(With.id("user_login"))
    element = wordpress.ui.element(With.name("log"))
    element = wordpress.ui.element(With.class_name("input"))
    element = wordpress.ui.element(With.tag_name("input"))

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    element = wordpress.ui.element(With.link_text("Lost your password?"))
    element = wordpress.ui.element(With.link_ptext("password"))

    wordpress.quit()


@test
def test_xpath(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()

    # Based on Text
    element = wordpress.ui.element(With.xpath("//*[text() = 'Lost your password?']"))

    # Based on partial text
    element = wordpress.ui.element(With.xpath("//*[contains(text(), 'Lost')]"))

    # Based on Title
    element = wordpress.ui.element(With.xpath("//*[@title = 'Password Lost and Found']"))

    # Based on Value
    element = wordpress.ui.element(With.xpath("//*[@value = 'Log In']"))

    # Based on any attribute e.g. for
    element = wordpress.ui.element(With.xpath("//*[@for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.ui.element(With.xpath("//*[contains(@for, '_login')]"))

    # Based on element type
    element = wordpress.ui.element(With.xpath("//*[@type ='password']"))

    wordpress.quit()


@test
def test_css_selector(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()

    # Based on any attribute e.g. for
    element = wordpress.ui.element(With.css_selector("*[for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.ui.element(With.css_selector("*[for *= '_login']"))

    # Based on element type
    element = wordpress.ui.element(With.css_selector("*[type ='password']"))

    # Based on compound classes
    element = wordpress.ui.element(With.css_selector(".button.button-large"))

    wordpress.quit()


@test
def test_arjuna_exts(my, request):
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()

    # Based on Text
    element = wordpress.ui.element(With.text("Lost your password?"))

    # Based on partial text
    element = wordpress.ui.element(With.ptext("Lost"))

    # Based on Title
    element = wordpress.ui.element(With.title("Password Lost and Found"))

    # Based on Value
    element = wordpress.ui.element(With.value("Log In"))

    # Based on any attribute e.g. for
    element = wordpress.ui.element(With.attr_value("for", "user_login"))

    # Based on partial content of an attribute
    element = wordpress.ui.element(With.attr_pvalue("for", "_login"))

    # Based on element type
    element = wordpress.ui.element(With.type("password"))

    # Based on compound classe
    element = wordpress.ui.element(With.compound_class("button button-large"))

    # Based on class names
    element = wordpress.ui.element(With.class_names("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.ui.element(With.point(Screen.xy(1043, 458)))

    # With Javascript
    element = wordpress.ui.element(With.javascript("return document.getElementById('wp-submit')"))

    wordpress.quit()