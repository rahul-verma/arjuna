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

from .action import *
from .endpoint import AnonHttpEndPoint, HttpEndPoint

class HttpEndPointLoader:

    def __init__(self, service):
        self._service = service
        self._anon_ep = None

    def __getattr__(self, ep_name: str, **fargs) -> HttpEndPointAction:
        if ep_name == "_anon":
            if vars(self)['_anon_ep'] is None:
                vars(self)['_anon_ep']  = AnonHttpEndPoint(service=vars(self)['_service'])
            mep = vars(self)['_anon_ep']
        else:
            mep = HttpEndPoint(vars(self)["_service"], name=ep_name, **fargs)
        return mep

    def send(self, **fargs):
        self._anon.send(**fargs)