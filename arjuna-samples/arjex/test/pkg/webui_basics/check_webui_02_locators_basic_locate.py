# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna import *

@test
def check_basic_identifiers_factory(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    wordpress.element(id="user_login")
    wordpress.element(name="log")
    wordpress.element(tags="input")
    wordpress.element(classes="input")

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    wordpress.element(link="password")
    # Full Link text match
    wordpress.element(flink="Lost your password?")


@test
def check_basic_identifiers_using_locate(request, wordpress):
    wordpress.locate(GuiWidgetDefinition(id="user_login"))