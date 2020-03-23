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
from arjex.lib.gns_adv.app_page_section.app import WordPress


@for_module
def dashboard_coded_re(request):
    # Setup
    wordpress = WordPress(section_dir="simple")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@for_test
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
def check_widget_coded_root_label(request, dashboard_coded_re):
    '''
        Left Nav has root element passed in __init__. No root in GNS.
    '''
    dashboard = dashboard_coded_re
    expected_src = '<div id="wpwrap"> </div>'
    request.asserter.assert_equal(dashboard.element(xpath="//div").source.content.root, expected_src, "Source of First div with Automator")

    expected_src = '<div class="wp-menu-arrow"/>'
    request.asserter.assert_equal(dashboard.left_nav_coded_root_label.gns.first_div.source.content.root, expected_src, "Source of First div with Widget WITH Root")
    request.asserter.assert_equal(dashboard.left_nav_coded_root_label.element(xpath="//div").source.content.root, expected_src, "Source of First div with Widget WITH Root")


@test
def check_widget_coded_root_locator(request, dashboard_coded_re):
    '''
        Left Nav has root element passed in __init__. No root in GNS.
    '''
    dashboard = dashboard_coded_re
    expected_src = '<div id="wpwrap"> </div>'
    request.asserter.assert_equal(dashboard.element(xpath="//div").source.content.root, expected_src, "Source of First div with Automator")

    expected_src = '<div class="wp-menu-arrow"/>'
    request.asserter.assert_equal(dashboard.left_nav_coded_root_locator.gns.first_div.source.content.root, expected_src, "Source of First div with Widget WITH Root")
    request.asserter.assert_equal(dashboard.left_nav_coded_root_locator.element(xpath="//div").source.content.root, expected_src, "Source of First div with Widget WITH Root")


@test
def check_widget_gns_root(request, dashboard_re):
    '''
        Left Nav has root element defined in GNS.
    '''
    dashboard = dashboard_re
    expected_src = '<div id="wpwrap"> </div>'
    request.asserter.assert_equal(dashboard.element(xpath="//div").source.content.root, expected_src, "Source of First div with Automator")

    expected_src = '<div class="wp-menu-arrow"/>'
    request.asserter.assert_equal(dashboard.left_nav.gns.first_div.source.content.root, expected_src, "Source of First div with Widget WITH Root")
    request.asserter.assert_equal(dashboard.left_nav.element(xpath="//div").source.content.root, expected_src, "Source of First div with Widget WITH Root")

