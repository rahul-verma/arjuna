# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from arjex.lib.gns_adv.app_page_section.app import WordPress

@for_test
def home(request):
    # Setup
    wordpress = WordPress(section_dir="withx")
    home = wordpress.launch()
    yield home

    # Teadown
    wordpress.quit()

@test
def check_diff_locator_or(request, home):
    e = home.gns.diff_locator_or
    print(e.source.content.root)

@test
def check_same_locator_or(request, home):
    e = home.gns.same_locator_or
    print(e.source.content.root)