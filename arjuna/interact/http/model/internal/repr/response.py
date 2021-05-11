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

from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.interact.http.model.internal.processor.response import HttpExpectedResProcessor, HttpUnexpectedResProcessor

class HttpResponseYamlRepr:

    def __init__(self, session, resp_yaml):
        self.__xproc = None
        self.__unexproc = None
        
        if "unexpected" in resp_yaml:
            self.__unexproc = HttpUnexpectedResProcessor(session, CIStringDict(resp_yaml["unexpected"]))
            del resp_yaml["unexpected"]

        self.__xproc = HttpExpectedResProcessor(session, CIStringDict(resp_yaml))

    def validate(self, response):
        if self.__xproc:
            self.__xproc.validate(response)
        if self.__unexproc:
            self.__unexproc.validate(response)
