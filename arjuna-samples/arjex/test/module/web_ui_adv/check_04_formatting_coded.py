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
def check_fmt_coded(request, logged_in_wordpress):
    logged_in_wordpress.format(text="Media").element(link="$text$").click()

@test
def check_fmt_config_coded(request, logged_in_wordpress):
    logged_in_wordpress.element(link="$C.link.name$").click()

@test
def check_fmt_reference_coded(request, logged_in_wordpress):
    logged_in_wordpress.element(link="$R.links.test1.navlink$").click()

@test
def check_fmt_reference_l10n_coded(request, logged_in_wordpress):
    logged_in_wordpress.element(link="$L.links.posting$").click()

@test
def check_fmt_coded_fmt_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(Formatter(text="Media").locator(link="$text$")).click()

@test
def check_fmt_config_coded_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(Locator(link="$C.link.name$")).click()

@test
def check_fmt_reference_coded_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(Locator(link="$R.links.test1.navlink$")).click()

@test
def check_fmt_reference_l10n_coded_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(Locator(link="$L.links.posting$")).click()