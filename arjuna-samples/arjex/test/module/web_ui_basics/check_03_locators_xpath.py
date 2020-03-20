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


@test
def check_xpath(request, wordpress):
    # Based on Text
    wordpress.element(xpath="//*[text() = 'Lost your password?']")

    # Based on partial text
    wordpress.element(xpath="//*[contains(text(), 'Lost')]")

    # Based on Title
    wordpress.element(xpath="//*[@title = 'Password Lost and Found']")

    # Based on Value
    wordpress.element(xpath="//*[@value = 'Log In']")

    # Based on any attribute e.g. for
    wordpress.element(xpath="//*[@for = 'user_login']")

    # Based on partial content of an attribute
    wordpress.element(xpath="//*[contains(@for, '_login')]")

    # Based on element type
    wordpress.element(xpath="//*[@type ='password']")
