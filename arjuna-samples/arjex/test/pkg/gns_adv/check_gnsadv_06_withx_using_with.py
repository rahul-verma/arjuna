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
def dashboard(request):
    # Setup
    wordpress = WordPress(section_dir="withx")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@test
def check_withx_using_with(request, dashboard):
    dashboard.left_nav.element(nav_link=nvpairs(lname="Posts")).click()
    dashboard.left_nav.element(nav_link=nvpairs(lname="Media")).click()
    dashboard.left_nav.element(nav_link=nvpairs(lname="Pages")).click()
    dashboard.left_nav.element(nav_link=nvpairs(lname="Comments")).click()