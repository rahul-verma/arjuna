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
    '''
        For this fixture:
        Wordpress related user options have been added to the project.conf
        You should replace the details with those corresponding to your own deployment of WordPress.
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
        }
    '''

    # Setup
    wp_url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def test_basic_identifiers(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    element = wordpress.element(With.id("user_login"))
    element = wordpress.element(With.name("log"))
    element = wordpress.element(With.tag("input"))
    element = wordpress.element(With.classes("input"))

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    element = wordpress.element(With.link("password"))
    # Full Link text match
    element = wordpress.element(With.flink("Lost your password?"))


@test
def test_xpath(request, wordpress):
    # Based on Text
    element = wordpress.element(With.xpath("//*[text() = 'Lost your password?']"))

    # Based on partial text
    element = wordpress.element(With.xpath("//*[contains(text(), 'Lost')]"))

    # Based on Title
    element = wordpress.element(With.xpath("//*[@title = 'Password Lost and Found']"))

    # Based on Value
    element = wordpress.element(With.xpath("//*[@value = 'Log In']"))

    # Based on any attribute e.g. for
    element = wordpress.element(With.xpath("//*[@for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.element(With.xpath("//*[contains(@for, '_login')]"))

    # Based on element type
    element = wordpress.element(With.xpath("//*[@type ='password']"))


@test
def test_selector(request, wordpress):

    # Based on any attribute e.g. for
    element = wordpress.element(With.selector("*[for = 'user_login']"))

    # Based on partial content of an attribute
    element = wordpress.element(With.selector("*[for *= '_login']"))

    # Based on element type
    element = wordpress.element(With.selector("*[type ='password']"))

    # Based on compound classes
    element = wordpress.element(With.selector(".button.button-large"))


@test
def test_arjuna_exts(request, wordpress):

    # Based on partial text
    element = wordpress.element(With.text("Lost"))

    # Based on Full Text
    element = wordpress.element(With.ftext("Lost your password?"))

    # Based on Title
    element = wordpress.element(With.title("Password Lost and Found"))

    # Based on Value
    element = wordpress.element(With.value("Log In"))

    # Based on partial match of content of an attribute
    element = wordpress.element(With.attr("for", "_login"))

    # Based on full match of an attribute
    element = wordpress.element(With.fattr("for", "user_login"))    

    # Based on element type
    element = wordpress.element(With.type("password"))

    # Based on compound classe
    element = wordpress.element(With.classes("button button-large"))
    element = wordpress.element(With.classes("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.element(With.point(Screen.xy(1043, 458)))

    # With Javascript
    element = wordpress.element(With.js("return document.getElementById('wp-submit')"))


@test
def test_wp_login(request, wordpress):
    '''
        For this test:
        Wordpress related user options have been added to the project.conf
        You should replace the details with those corresponding to your own deployment of WordPress.
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
	        wp.logout.url = ${userOptions.wp.app.url}"/wp-login.php?action=logout"

            wp.admin {
                name = "<username>"
                pwd = "<password>"
            }
        }
    '''

    user = wordpress.config.get_user_option_value("wp.admin.name").as_str()
    pwd = wordpress.config.get_user_option_value("wp.admin.pwd").as_str()
    
    # Login
    user_field = wordpress.element(With.id("user_login"))
    user_field.text = user

    pwd_field = wordpress.element(With.id("user_pass"))
    pwd_field.text = pwd

    submit = wordpress.element(With.id("wp-submit"))
    submit.click()

    wordpress.element(With.classes("welcome-view-site"))

    # Logout
    url = wordpress.config.get_user_option_value("wp.logout.url").as_str()
    wordpress.go_to_url(url)

    confirmation = wordpress.element(With.link("log out"))
    confirmation.click()

    wordpress.element(With.text("logged out"))

@test
def test_wp_login_concise(request, wordpress):
    
    user = wordpress.config.get_user_option_value("wp.admin.name").as_str()
    pwd = wordpress.config.get_user_option_value("wp.admin.pwd").as_str()
    
    # Login
    wordpress.element(With.id("user_login")).text = user
    wordpress.element(With.id("user_pass")).text = pwd
    wordpress.element(With.id("wp-submit")).click()
    wordpress.element(With.classes("welcome-view-site"))

    # Logout
    url = wordpress.config.get_user_option_value("wp.logout.url").as_str()
    wordpress.go_to_url(url)
    wordpress.element(With.link("log out")).click()
    wordpress.element(With.text("logged out"))
