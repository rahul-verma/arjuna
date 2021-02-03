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
from arjex.lib.gns_adv.app.wp import WordPress

@for_module
def wordpress(request):
    wordpress = WordPress()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def check_nested_element_gns_gns(request, wordpress):
    # Locate the form and then all input elements

    # Level 1 - Element from App
    form = wordpress.gns.login_form

    # Level 2 - Element in Element
    user_box = form.gns.first_input
    print(user_box.source.content.all)

    # Level 2 - MultiElement in Element
    labels = form.gns.labels

    for label in labels:
        print(label.text)
        print(label.source.content.all)

        # Level 3 - Element in Partial Element
        i = label.gns.first_input
        print(i.source.content.all)
