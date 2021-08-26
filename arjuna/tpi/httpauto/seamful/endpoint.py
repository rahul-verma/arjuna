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

class BaseHttpEndPoint:

    def __init__(self, *, name, service, ep_dir):
        self.__name = name
        self.__service = service
        self.__root_dir = ep_dir
        from .actionloader import HttpActionLoader
        self.__actions = HttpActionLoader(endpoint=self)

    @property
    def name(self):
        return self.__name

    @property
    def service(self):
        return self.__service

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    def message(self):
        '''
            Http Message Loader for this service using default end point.
        '''
        return self.action._anon.message

    @property
    def action(self):
        '''
            Http Message Loader for this service end point.
        '''
        return self.__actions

    def send(self, msg_name=None, **fargs) -> HttpResponse:
        return self.action._anon.send(msg_name=msg_name, **fargs)

    def perform(self, action_name, **fargs) -> HttpResponse:
        getattr(self.__actions, action_name).perform()

class AnonHttpEndPoint(BaseHttpEndPoint):

    def __init__(self, *, service):
        super().__init__(name="anon", service=service, ep_dir=service.root_dir)

class HttpEndPoint(BaseHttpEndPoint):
    def __init__(self, *, name, service):
        super().__init__(name=name, service=service, ep_dir=os.path.join(service.root_dir, name))

