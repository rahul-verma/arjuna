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

import json
import ast
import abc
import os
import time
from urllib.parse import urlparse, urlencode, parse_qs, quote
from requests import Request, Session
from arjuna.tpi.error import HttpUnexpectedStatusCodeError, HttpSendError
from arjuna.tpi.parser.json import Json
from arjuna.tpi.parser.html import Html
from arjuna.tpi.engine.asserter import AsserterMixIn
from arjuna.tpi.helper.arjtype import CIStringDict
from requests.exceptions import ConnectionError, TooManyRedirects
from arjuna.tpi.engine.asserter import AsserterMixIn

safe_eval = ast.literal_eval

def _convert_yaml_json_to_json(jval):
    def handle_str_val(in_val):
        if in_val.lower().strip() == "null":
            out_val = "null"
        else:
            # The string could be a variable name. With spaces, it will be treated as Python statement.
            if in_val in locals() or in_val in globals():
                out_val = in_val
            else:
                try:
                    out_val = safe_eval(in_val)
                except (NameError, SyntaxError, ValueError): # The string is evaluated as a variable name or Python statement
                    out_val = jval
        return out_val

    if type(jval) is dict:
        # This is needed if e.g. "1" is a string and not to be treated as a number. In this case type: str should be coded.
        if "value" in jval:
            raw_value = jval["value"]
            if "type" in jval:
                jtype = jval["type"].lower().strip()
                allowed_set = {"str", "dict", "list", "int", "float", "bool"}
                if jtype in allowed_set:
                    jval = eval(jtype)(jval["value"])
                else:
                    raise Exception("type can be specified only as one of {}".format(allowed_set))
            elif type(raw_value) is str:
                jval = handle_str_val(raw_value)
            else:
                jval = raw_value
        else:
            jval = jval
    elif type(jval) is str:
        jval = handle_str_val(jval)
    else:
        jval = jval

    return jval

class _HttpYamlReqRepr:

    def __init__(self, session, req_yaml):
        if "method" in req_yaml:     
            self.__method = req_yaml["method"]
            del req_yaml["method"]
        else:
            self.__method = "get"

        if "route" in req_yaml:     
            self.__route = req_yaml["route"]
            del req_yaml["route"]
        else:
            self.__route = "/"

        if "content_type" in req_yaml:
            from arjuna import Http
            if "content" in req_yaml:
                if req_yaml["content_type"] == "json":
                    req_yaml["content"] = _convert_yaml_json_to_json(req_yaml["content"])

                if req_yaml["content"] is None:
                    req_yaml["content"] == "null"

                req_yaml["content"] = getattr(Http.content, req_yaml["content_type"].lower())(req_yaml["content"])
            del req_yaml["content_type"]

        self.__attrs = req_yaml

    @property
    def method(self):
        return self.__method

    @property
    def route(self):
        return self.__route

    @property
    def attrs(self):
        return self.__attrs

class _HttpResProcessor(metaclass=abc.ABCMeta):
    
    def __init__(self, session, codes=200, url=None, headers=None, text=None, json={}):
        from .request import _HttpRequest
        self.__session = session
        self.__json_set = False
        if json:
            self.__json_set = True

        self.__repr = {
            "codes" : _HttpRequest._process_codes(codes),
            "url" : url,
            "headers": {},
            "text": {
                "partials": None,
                "patterns": None
            },
            "json": {
                "type": None,
                "size": None,
                "min_size": None,
                "max_size": None,
                "size_range": None,
                "schema": None,
                "jpaths": {}
            },
        }

        for k,v in json.items():
            if k in self.__repr["json"]:
                self.__repr["json"][k] = json[k]        

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
    def json(self):
        if self.__json_set:
            return self.__repr["json"]

    @abc.abstractmethod
    def validate(self, response):
        pass

class JsonValidator(AsserterMixIn):

    def __init__(self, response, json_yaml):
        super().__init__()
        if "jpaths" in json_yaml:
            for jpath, jval in json_yaml["jpaths"].items():
                try:
                    val = response.find(jpath)
                except Exception as e:
                    if str(e).startswith("Parse error"):
                        raise Exception("Wrong JPath syntax: {}".format(jpath))
                    raise
                jval = _convert_yaml_json_to_json(jval)
                self.asserter.assert_equal(val, jval, "Dummy msg") # msg should reflect label or file name

class _HttpExpectedResProcessor(_HttpResProcessor):
    
    def __init__(self, session, conditions_dict):
        print(conditions_dict)
        super().__init__(session, **conditions_dict)

    def validate(self, response):
        self._session._validate_status_code(response, self.codes)
        if self.url:
            assert response.request.url == self.url 
        if self.json:
            jvalidator = JsonValidator(response.json, self.json)   

class _HttpUnexpectedResProcessor(_HttpResProcessor):

    def __init__(self, session, conditions_dict):
        super().__init__(session, **conditions_dict)

    def validate(self, response):
        self._session._validate_status_code(response, self.codes, expected=False)

class _HttpYamlResProcessor:

    def __init__(self, session, resp_yaml):
        print(resp_yaml)
        self.__xproc = None
        self.__unexproc = None
        if "expected" in resp_yaml:
            self.__xproc = _HttpExpectedResProcessor(session, CIStringDict(resp_yaml["expected"]))
        
        if "unexpected" in resp_yaml:
            self.__unexproc = _HttpUnexpectedResProcessor(session, CIStringDict(resp_yaml["unexpected"]))

    def validate(self, response):
        if self.__xproc:
            self.__xproc.validate(response)
        if self.__unexproc:
            self.__unexproc.validate(response)

class _HttpMessage:

    def __init__(self, session, req_repr, resp_processor):
        self.__session = session
        self.__req_repr = req_repr
        self.__resp_processor = resp_processor

    @property
    def _req(self):
        return self.__req_repr

    @property
    def _session(self):
        return self.__session

    def send(self):
        method = self._req.method
        try:
            call = getattr(self._session, method)
        except AttributeError:
            raise Exception(f"Unsupported HTTP method: {method}")
        else:
            response = call(self._req.route, **self._req.attrs)
            self.__resp_processor.validate(response)
            return response

    @classmethod
    def root(cls, session):
        req_repr = _HttpYamlReqRepr(session, CIStringDict())
        resp_proc = _HttpYamlResProcessor(session, CIStringDict())
        return _HttpMessage(session, req_repr, resp_proc)

    @classmethod
    def from_file(cls, session, msg_file_name, **fargs):
        # Process Yaml file
        from arjuna import C, Yaml
        file_path = os.path.join(C("httpauto.message.dir"), msg_file_name + ".yaml")
        f = open(file_path, "r")
        msg_yaml = f.read()
        f.close()
        from arjuna.core.fmt import arj_format_str, arj_convert
        # Convert Arjuna custom objects to raw Python objects before formatting.
        fargs = {k:arj_convert(v) for k,v in fargs.items()}
        msg_yaml = arj_format_str(msg_yaml, tuple(), fargs)
        msg_yaml = Yaml.from_str(msg_yaml, allow_any=True)
        if msg_yaml is None:
            return cls.root(session)

        print(msg_yaml)
        if "request" in msg_yaml:
            req_repr = _HttpYamlReqRepr(session, CIStringDict(msg_yaml["request"].as_map()))
        else:
            req_repr = _HttpYamlReqRepr(session, CIStringDict())
        
        if "response" in msg_yaml:
            resp_proc = _HttpYamlResProcessor(session, CIStringDict(msg_yaml["response"].as_map()))
        else:
            resp_proc = _HttpYamlResProcessor(session, CIStringDict())

        return _HttpMessage(session, req_repr, resp_proc)


class HttpPacket(AsserterMixIn, metaclass=abc.ABCMeta):

    def __init__(self, http_msg):
        super().__init__()
        self.__http_msg = http_msg

    @property
    def headers(self) -> dict:
        ''' 
            HTTP Headers for this message.
        '''
        return self.__http_msg.headers

    def assert_empty_content(self, *, msg):
        '''
            Validates if content is empty.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if self.headers['Content-Length'] != '0':
            raise AssertionError("Content is not empty.")

    def assert_non_empty_content(self, *, msg):
        '''
            Validates if content is empty.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if self.headers['Content-Length'] == '0':
            raise AssertionError("Content is empty.")

    def assert_header_match(self, header, value=None, *, msg):
        '''
            Validates the presence and optionally the value of an HTTP Header.

            Arguments:
                header: Name of header
                value: Text contained in header. If not provided, then only presence of header is checked.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if header not in self.headers:
            raise AssertionError(f">>{header}<< not present in HTTP Request. {msg}")

        if value is not None:
            actual = self.headers[header]
            if actual != value:
                raise AssertionError(f"Value >>header<< is {actual} but was expected to be {value}. {msg}.")

    def assert_header_mismatch(self, header, value=None, *, msg):
        '''
            Validates the absence of header or mismatch of its content with provided value.

            Arguments:
                header: Name of header
                value: Text contained in header. If not provided, then only absence of header is checked.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''

        if value is None:
            if header in self.headers:
                raise AssertionError(f">>{header}<< is present in HTTP Request. {msg}")
        else:
            actual = self.headers[header]
            if actual == value:
                raise AssertionError(f"Value >>header<< is {actual}. It was expected to be different. {msg}.")

