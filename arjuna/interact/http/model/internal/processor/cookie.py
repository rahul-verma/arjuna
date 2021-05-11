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

from arjuna.tpi.engine.asserter import AsserterMixIn

class CookieValidator(AsserterMixIn):

    def __init__(self, session, cookie_yaml):
        super().__init__()
        for cookie_name, cookie_val in cookie_yaml.items():
            msg = f"Cookie with name {cookie_name} was not found in session cookies."
            try:
                self.asserter.assert_true(cookie_name in session.cookies, msg=msg)
            except AssertionError:
                self.asserter.fail(msg=msg)
            attr_map = {
                "secure": None,
                "HttpOnly": None
            }
            cookie_val_to_match = None
            if type(cookie_val) is dict:
                for k,v in cookie_val.items():
                    if k in raw_map:
                        raw_map[k] = v
                if "value" in cookie_val:
                    cookie_val_to_match = cookie_val["value"]
            else:
                cookie_val_to_match = str(cookie_val)
