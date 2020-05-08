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

@for_module
def dashboard(request):
    # Setup
    wordpress = WordPress(section_dir="simple")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@for_module
def dashboard_re(request):
    # Setup
    wordpress = WordPress(section_dir="root_anchor")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@test
def check_wait_until_absent_without_root_1(request, dashboard):
    # Should be validated in root element.
    dashboard.left_nav.gns.menu.gns.wait_until_absent("non_existing")

    try:
        # It is present
        dashboard.left_nav.gns.menu.gns.wait_until_absent("settings")
    except GuiWidgetForLabelPresentError as e:
        print("Exception as Expected")
        print(str(e))
    except Exception as e:
        raise Exception("Unexpected exception raise: ", str(e))
    else:
        raise Exception("Exception not raised.")

@test
def check_wait_until_absent_without_root_2(request, dashboard):
    # Should be validated in root element.
    dashboard.left_nav.gns.menu.wait_until_absent(id="something")

    try:
        # It is present
        dashboard.left_nav.gns.menu.wait_until_absent(link="Settings")
    except GuiWidgetPresentError as e:
        print("Exception as Expected")
        print(str(e))
    except Exception as e:
        raise Exception("Unexpected exception raise: ", str(e))
    else:
        raise Exception("Exception not raised.")

@test
def check_contains_without_root_1(request, dashboard):
    # Should be validated in root element.
    print(dashboard.left_nav.gns.menu.gns.contains("settings"))
    print(dashboard.left_nav.gns.menu.gns.contains("non_existing"))

@test
def check_contains_without_root_2(request, dashboard):
    # Should be validated in root element.
    print(dashboard.left_nav.gns.menu.contains(link="Settings"))
    print(dashboard.left_nav.gns.menu.contains(id="something"))

@test
def check_wait_until_absent_with_root_1(request, dashboard_re):
    # Should be validated in root element.
    dashboard_re.left_nav.gns.wait_until_absent("non_existing")

    try:
        # It is present
        dashboard_re.left_nav.gns.wait_until_absent("settings")
    except GuiWidgetForLabelPresentError as e:
        print("Exception as Expected")
        print(str(e))
    except Exception as e:
        raise Exception("Unexpected exception raise: ", str(e))
    else:
        raise Exception("Exception not raised.")

@test
def check_wait_until_absent_with_root_2(request, dashboard_re):
    # Should be validated in root element.
    dashboard_re.left_nav.wait_until_absent(id="something")

    try:
        # It is present
        dashboard_re.left_nav.wait_until_absent(link="Settings")
    except GuiWidgetPresentError as e:
        print("Exception as Expected")
        print(str(e))
    except Exception as e:
        raise Exception("Unexpected exception raise: ", str(e))
    else:
        raise Exception("Exception not raised.")

@test
def check_contains_with_root_1(request, dashboard_re):
    # Should be validated in root element.
    print(dashboard_re.left_nav.gns.contains("settings"))
    print(dashboard_re.left_nav.gns.contains("non_existing"))

@test
def check_contains_with_root_2(request, dashboard_re):
    # Should be validated in root element.
    print(dashboard_re.left_nav.contains(tag="div"))
    print(dashboard_re.left_nav.contains(id="something"))