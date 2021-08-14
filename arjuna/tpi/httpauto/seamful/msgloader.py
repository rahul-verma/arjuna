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

from .message import RootHttpMessage, HttpMessage

class HttpMessageLoader:

    def __init__(self, action):
        self._action = action

    def __getattr__(self, msg_name: str, **fargs) -> HttpMessage:
        if msg_name == "root":
            msg = RootHttpMessage(vars(self)["_action"])
        else:
            msg = HttpMessage(name=msg_name, action=vars(self)["_action"], **fargs)

        return msg

    def send(self, msg_name=None, **fargs):
        if msg_name is None:
            return self.root.send(**fargs)
        else:
            return getattr(self, msg_name).send(**fargs)