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
from .json.validator import ExpectedJsonValidator, UnexpectedJsonValidator
from .cookie.validator import CookieValidator
from .text.validator import ExpectedTextValidator, UnexpectedTextValidator
from .header.store import HeaderExtractor
from .text.store import TextExtractor
from .xml.store import XmlExtractor
from .validator import Validator
from arjuna.interact.http.model.internal.helper.yaml import convert_yaml_obj_to_content
from arjuna.tpi.engine.asserter import AsserterMixIn

class _HttpResProcessor(AsserterMixIn, metaclass=abc.ABCMeta):
    
    def __init__(self, session, codes=None, url=None, headers={}, cookies={}, has={}, match={}, store={}, validate={}):
        super().__init__()
        self.__session = session
        self.__match_set = False
        self.__has_set = False
        self.__store_set = False
        self.__validate_set = False
        if has:
            self.__has_set = True
        if match:
            self.__match_set = True
        if store:
            self.__store_set = True
        if validate:
            self.__validate_set = True

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
            },
            "store": store,
            "validate": validate
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

        store_var_dict = {"jpath":{}, "regex":{}, "xpath":{}, "header":{}, "cookie":{}}
        import copy
        for k,v in store.items():
            self.__repr["store"][k] = copy.deepcopy(store_var_dict)
            for k2, v2 in v.items():
                if k2 in self.__repr["store"][k]:
                    self.__repr["store"][k][k2] = v2   

        for k in self.__repr["validate"]:
            if k not in self.__repr["store"]:
                raise Exception(f"{k} in validate section is not defined in store section of message.") 

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

    @property
    def store(self):
        if self.__store_set:
            return self.__repr["store"]

    @property
    def validations(self):
        if self.__validate_set:
            return self.__repr["validate"]

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
        if self.store:
            for name, sdict in self.store.items():
                if sdict["header"]:
                    HeaderExtractor(response).store(name, sdict["header"])
                elif sdict["regex"]:
                    TextExtractor(response).store(name, sdict["regex"])
                elif sdict["xpath"]:
                    XmlExtractor(response).store(name, sdict["xpath"])
        if self.validations:
            validator = Validator(response)
            for k, target in self.validations.items():
                validator.validate(k, target)

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
            response.assert_headers(headers, msg="One or more headers do not match expected values.") 
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
                    self.asserter.assert_not_equal(response.headers[k], v, f"HTTP response header >>{k}<< value matches >>{v}<< which is unexpected.")
