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

import abc
from .json import ExpectedJsonValidator, UnexpectedJsonValidator
from .cookie import CookieValidator
from .text import ExpectedTextValidator, UnexpectedTextValidator
from arjuna.interact.http.model.internal.helper.yaml import convert_yaml_obj_to_content
from arjuna.tpi.engine.asserter import AsserterMixIn

class _HttpResProcessor(AsserterMixIn, metaclass=abc.ABCMeta):
    
    def __init__(self, session, codes=None, url=None, headers={}, cookies={}, has={}, match={}):
        super().__init__()
        self.__session = session
        self.__match_set = False
        self.__has_set = False
        if has:
            self.__has_set = True
        if match:
            self.__match_set = True

        self.__repr = {
            "codes" : None,
            "url" : url,
            "headers": headers,
            "cookies": cookies,
            "has": {
                "jpath": None,
                "regex": None,
                "partial": None
            },
            "match": {
                "jpath": None,
                "regex": None,
            }
        }

        from arjuna.tpi.httpauto.request import _HttpRequest
        if codes is not None:
            self.__repr["codes"] = _HttpRequest._process_codes(codes)

        for k,v in has.items():
            if k in self.__repr["has"]:
                self.__repr["has"][k] = has[k]   

        for k,v in match.items():
            if k in self.__repr["match"]:
                self.__repr["match"][k] = match[k]   

        print(self.__repr) 

    @property
    def _session(self):
        return self.__session

    @property
    def codes(self):
        return self.__repr["codes"]

    @property
    def url(self):
        return self.__repr["url"]

    @property
    def headers(self):
        return self.__repr["headers"]

    @property
    def cookies(self):
        return self.__repr["cookies"]

    @property
    def match(self):
        if self.__match_set:
            return self.__repr["match"]

    @property
    def has(self):
        if self.__has_set:
            return self.__repr["has"]

    @abc.abstractmethod
    def _validate(self, response):
        pass

    @abc.abstractmethod
    def _get_text_validator(self, response):
        pass

    @abc.abstractmethod
    def _get_json_validator(self, response):
        pass

    def validate(self, response):
        self._validate(response)
        if self.has:
            if self.has["jpath"]:
                self._get_json_validator(response).assert_has_patterns(self.has["jpath"])
            if self.has["regex"]:
                self._get_text_validator(response).assert_has_patterns(self.has["regex"])
        if self.match:
            if self.match["jpath"]:
                self._get_json_validator(response).assert_match_for_patterns(self.match["jpath"])
            if self.match["regex"]:
                self._get_text_validator(response).assert_match_for_patterns(self.match["regex"])
        # if self.text:
        #     self._get_text_validator(response, self.text).validate()

class HttpExpectedResProcessor(_HttpResProcessor):
    
    def __init__(self, session, conditions_dict):
        super().__init__(session, **conditions_dict)
        self.__text_validator = None
        self.__json_validator = None

    def _get_text_validator(self, response):
        if self.__text_validator is None:
            self.__text_validator = ExpectedTextValidator(response.text) 
        return self.__text_validator

    def _get_json_validator(self, response):
        if self.__json_validator is None:
            self.__json_validator = ExpectedJsonValidator(response.json) 
        return self.__json_validator

    def _validate(self, response):
        if self.codes:
            self._session._validate_status_code(response, self.codes)
        if self.url:
            assert response.request.url == self.url 
        if self.headers:
            headers = {k:str(v) for k,v in  convert_yaml_obj_to_content(self.headers).items()}
            response.assert_headers(self.headers, msg="dummy") 
        if self.cookies:
            CookieValidator(self._session, convert_yaml_obj_to_content(self.cookies))

class HttpUnexpectedResProcessor(_HttpResProcessor):

    def __init__(self, session, conditions_dict):
        super().__init__(session, **conditions_dict)
        self.__text_validator = None
        self.__json_validator = None

    def _get_text_validator(self, response):
        if self.__text_validator is None:
            self.__text_validator = UnexpectedTextValidator(response.text) 
        return self.__text_validator

    def _get_json_validator(self, response):
        if self.__json_validator is None:
            self.__json_validator = UnexpectedJsonValidator(response.json) 
        return self.__json_validator

    def _validate(self, response):
        if self.codes:
            self._session._validate_status_code(response, self.codes, expected=False)
        if self.headers:
            headers = {k:str(v) for k,v in  convert_yaml_obj_to_content(self.headers).items()}
            for k,v in headers.items():
                if k in response.headers:
                    self.asserter.assert_not_equal(response.headers[k], v, f"HTTP response header {k} value matches {v} which is unexpected.")
