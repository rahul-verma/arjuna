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

from arjuna.interact.http.model.internal.helper.yaml import convert_yaml_obj_to_content

class HttpRequestYamlRepr:

    def __init__(self, session, req_yaml, *, label):
        self.__label = label
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
            content_handler = getattr(Http.content, req_yaml["content_type"].lower())
            del req_yaml["content_type"]
        else:
            content_handler = session.request_content_handler

        if "content" in req_yaml:
            req_yaml["content"] = convert_yaml_obj_to_content(req_yaml["content"])
            # if req_yaml["content"] is None:
            #     req_yaml["content"] == "null"

            req_yaml["content"] = content_handler(req_yaml["content"])

        self.__attrs = req_yaml

    @property
    def label(self):
        return self.__label

    @property
    def method(self):
        return self.__method

    @property
    def route(self):
        return self.__route

    @property
    def attrs(self):
        return self.__attrs
