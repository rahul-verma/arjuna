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

class HttpActionLoader:

    def __init__(self, endpoint):
        self._endpoint = endpoint

    def __getattr__(self, action: str, **fargs) -> HttpEndPointAction:
        if action == "_anon":
            msg = AnonEndPointAction(endpoint=vars(self)["_endpoint"])
        else:
            msg = HttpEndPointAction(name=action, endpoint=vars(self)["_endpoint"], **fargs)
        return msg

    def perform(self, **fargs):
        self._anon.perform(**fargs)