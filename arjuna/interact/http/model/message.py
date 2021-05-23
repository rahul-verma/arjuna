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
from .internal.repr.request import HttpRequestYamlRepr
from .internal.repr.response import HttpResponseYamlRepr
from arjuna.tpi.helper.arjtype import CIStringDict

class HttpMessage:

    def __init__(self, session, req_repr, resp_processor):
        self.__session = session
        self.__req_repr = req_repr
        self.__resp_processor = resp_processor
        self.__label = req_repr.label

    @property
    def label(self):
        return self.__label

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
            response = call(self._req.route, label=self.label, **self._req.attrs)
            self.__resp_processor.validate(response)
            return response

    @classmethod
    def root(cls, session):
        req_repr = HttpRequestYamlRepr(session, CIStringDict(), label="Root")
        resp_proc = HttpResponseYamlRepr(session, CIStringDict())
        return HttpMessage(session, req_repr, resp_proc)

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

        if "label" in msg_yaml:
            label = msg_yaml["label"]
            del msg_yaml["label"]
        else: 
            label = msg_file_name

        if "request" in msg_yaml:
            req_repr = HttpRequestYamlRepr(session, CIStringDict(msg_yaml["request"].as_map()), label=label)
            del msg_yaml["request"]
        else:
            req_repr = HttpRequestYamlRepr(session, CIStringDict(), label=label)
        
        resp_proc = HttpResponseYamlRepr(session, CIStringDict(msg_yaml.as_map()))

        return HttpMessage(session, req_repr, resp_proc)

