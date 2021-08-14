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

from .eploader import HttpEndPointLoader

class HttpService:
    '''
        Represents an HTTP Service.

        Keyword Arguments:
            session: HTTP Session associated with this service.
            name: (Optional) Name of service. Should have a corresponding named directory in Project root/httpauto/service directory. If not provided then the name is set to **mservice**
    '''

    def __init__(self, *, session, name="mservice"):
        self.__name = name
        self.__session = session
        from arjuna import C
        if name == "mservice":
            self.__root_dir = C("httpauto.dir")
        else:
            self.__root_dir = os.path.join(C("httpauto.dir"), "service/{}".format(name))
        self.__endpoints = HttpEndPointLoader(self)

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    def name(self):
        '''
            Name of service
        '''
        return self.__session

    @property
    def session(self):
        '''
            HTTP Session object associated with this service.
        '''
        return self.__session

    @property
    def ep(self):
        '''
            Http End Point loader for this service.
        '''
        return self.__endpoints

    @property
    def message(self):
        '''
            Http Message Loader for this service using default end point.
        '''
        return self.ep._anon.message

    @property
    def action(self):
        '''
            Http Action Loader for this service using default end point.
        '''
        return self.ep._anon.action

    def send(self, msg_name=None, **fargs) -> HttpResponse:
        '''
            Send an HTTP Message using this service using default end point.
        '''
        return self.ep._anon.send(msg_name=msg_name, **fargs)
    
    def perform(self, msg_name=None, **fargs) -> HttpResponse:
        '''
            Perform an HTTP Action using this service using default end point.
        '''
        return self.ep._anon.perform(msg_name=msg_name, **fargs)