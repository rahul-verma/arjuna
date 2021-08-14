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

from arjuna.tpi.httpauto.response import HttpResponse

class BaseHttpEndPointAction:

    def __init__(self, *, name, endpoint):
        self.__endpoint = endpoint
        from .msgloader import HttpMessageLoader
        self._messages = HttpMessageLoader(action=self)

    @property
    def message(self):
        return self._messages

    @property
    def endpoint(self):
        return self.__endpoint

    def send(self, msg_name=None, **fargs) -> HttpResponse:
        return self.message.send(msg_name, **fargs)

    def perform(self, action_name, **fargs) -> HttpResponse:
        pass

class AnonEndPointAction(BaseHttpEndPointAction):

    def __init__(self, *, endpoint):
        super().__init__(name="anonaction", endpoint=endpoint)

    def perform(self):
        pass

class HttpEndPointAction(BaseHttpEndPointAction):

    def __init__(self, *, name, endpoint, msg_loader):
        super().__init__(name=name, endpoint=endpoint)
        self.__action_dir = os.path.join(endpoint.root_dir, "action", name)

    def perform(self):
        pass