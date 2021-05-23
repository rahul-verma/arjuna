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
        cookies = session.parsed_cookies
        for cookie_name, cookie_val in cookie_yaml.items():
            msg = f"Cookie with name >>{cookie_name}<< was not found in session cookies."
            try:
                self.asserter.assert_true(cookie_name in session.cookies, msg=msg)
            except AssertionError:
                self.asserter.fail(msg=msg)

            cookie = cookies[cookie_name]

            if type(cookie_val) is dict:
                for k,v in cookie_val.items():
                    if k == "value":
                        self.asserter.assert_equal(cookie.value, cookie_val["value"], f"Cookie value for >>{cookie_name}<< does not match expected value.")
                    elif k.lower() == "httponly":
                        self.asserter.assert_true(cookie.httponly, f"Cookie >>{cookie_name}<< does not have >>HttpOnly flag<< set.")
                    elif k.lower() == "secure":
                        self.asserter.assert_true(cookie.secure, f"Cookie >>{cookie_name}<< does not have >>secure flag<< set.")
            else:
                self.asserter.assert_equal(cookie.value, str(cookie_val), f"Cookie value for >>{cookie_name}<< does not match expected value.")
