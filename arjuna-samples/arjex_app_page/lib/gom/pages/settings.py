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

from .basepage import WPBasePage

class Settings(WPBasePage):

    def validate_readiness(self):
        self.element("role").wait_until_visible()

    def tweak_role_value(self, value):
        role_select = self.dropdown("role")
        role_select.select_value(value)
        self.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))
