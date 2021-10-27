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

import os
from arjuna.interact.http.model.internal.repr.request import HttpRequestYamlRepr
from arjuna.interact.http.model.internal.repr.response import HttpResponseYamlRepr
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.tpi.error import SEAMfulMessageFileError
from arjuna.tpi.parser.text import Text

def check_data_arg_type(kwargs):
    from arjuna.tpi.data.entity import _DataEntity
    if 'data' in kwargs:
        if type(kwargs['data']) is not dict and not isinstance(kwargs['data'], _DataEntity):
            raise Exception("'data' keyword argument for HTTP message call or HTTP message.send() call can only be a Python dict or an Arjuna Data Entity. Provided: >>{}<< of type >>{}<<".format(kwargs['data'], type(kwargs['data'])))


class BaseHttpMessage:

    def __init__(self, name, action):
        self.__name = name
        self.__action = action

    @property
    def name(self):
        return self.__name

    @property
    def _action(self):
        return self.__action

    def send(self, **fargs):
        from arjuna import log_info
        log_info("Sending", self)
        check_data_arg_type(fargs)
        label, req_repr, resp_proc = self._load(**fargs)
        method = req_repr.method
        try:
            call = getattr(self._action._endpoint.service._session, method)
        except AttributeError:
            raise Exception(f"Unsupported HTTP method: {method}")
        else:
            response = call(req_repr.route, label=label, **req_repr.attrs)
            resp_proc.validate(response)
            return response

    def _load(self, **sfargs):
        pass

    def _get_file_path_msg(self):
        return ""

    def __str__(self):
        meta_str = f"HTTP Message >{self.name}<" + self._get_file_path_msg()
        if self._action.name != "anon":
            meta_str += f" for action >{self._action.name}<"
        if self._action._endpoint.name != "anon":
            meta_str += f" for end point >{self._action._endpoint.name}<"
        if self._action._endpoint.service.name != "anon":
            meta_str += f" for service >{self._action._endpoint.service.name}<"
        return meta_str

    __repr__ = __str__


class RootHttpMessage(BaseHttpMessage):

    def __init__(self, action):
        super().__init__(name="Root", action=action)

    def _load(self, **sfargs):
        req_repr = HttpRequestYamlRepr(self._action, CIStringDict(), label="Root")
        resp_proc = HttpResponseYamlRepr(self._action, CIStringDict())
        return "Root", req_repr, resp_proc

class HttpMessage(BaseHttpMessage):

    def __init__(self, *, name, action, **fargs):
        super().__init__(name=name, action=action, **fargs)
        check_data_arg_type(fargs)
        self.__fargs = fargs
        # Process Yaml file
        from arjuna import C, Yaml
        # Check Built-In Security Message
        my_dir = os.path.dirname(os.path.realpath(__file__))
        self.__action_file_path = os.path.abspath(os.path.join(my_dir, "..", "..","..", "res", "security", "http", "message", name + ".yaml"))
        try:
            f = open(self.__action_file_path, "r")
        except FileNotFoundError:
            self.__file_path = os.path.join(action._endpoint.root_dir, "message", name + ".yaml")
            try:
                f = open(self.__file_path, "r")
            except FileNotFoundError:
                raise SEAMfulMessageFileError(self, msg=f"Message file not found at location: {self.__file_path}")
        self.__msg_yaml = f.read()
        f.close()
        super().__init__(name=name, action=action)

    def _get_file_path_msg(self):
        return f" at ({self.__file_path})"

    def _load(self, **sfargs):
        from arjuna import C, Yaml
        margs = {}
        margs.update(self.__fargs)
        margs.update(sfargs)
        from arjuna.core.fmt import arj_convert
        margs = {k:arj_convert(v) for k,v in margs.items()}
        msg_yaml = Text(self.__msg_yaml).format(**margs)
        msg_yaml = Yaml.from_str(msg_yaml, allow_any=True)
        if msg_yaml is None:
            req_repr = HttpRequestYamlRepr(self._action, CIStringDict(), label="Root")
            resp_proc = HttpResponseYamlRepr(self._action, CIStringDict())
            return self.name, req_repr, resp_proc

        if "label" in msg_yaml:
            label = msg_yaml["label"]
            del msg_yaml["label"]
        else: 
            label = self.name

        if "request" in msg_yaml:
            req_repr = HttpRequestYamlRepr(self._action, CIStringDict(msg_yaml["request"].as_map()), label=label)
            del msg_yaml["request"]
        else:
            req_repr = HttpRequestYamlRepr(self._action, CIStringDict(), label=label)
        
        resp_proc = HttpResponseYamlRepr(self._action, CIStringDict(msg_yaml.as_map()))
        return label, req_repr, resp_proc








