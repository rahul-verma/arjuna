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
import importlib

from arjuna.tpi.httpauto.response import HttpResponse
from arjuna.tpi.error import SEAMfulActionFileError
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.tpi.data.entity import _DataEntity

class _HttpActionStep:

    def __init__(self, action, step_yaml):
        self.__action = action
        self.__step_yaml = step_yaml

    def perform(self, **fargs):
        return self.__action.send(self.__step_yaml, **fargs)

class _HttpActionSteps:

    def __init__(self, action, steps_yaml=None):
        self.__action = action
        self.__steps = steps_yaml is not None and steps_yaml or []

    def __iter__(self):
        return iter([_HttpActionStep(self.__action, step_yaml) for step_yaml in self.__steps])

class BaseHttpEndPointAction:

    def __init__(self, *, name, endpoint):
        self.__name = name
        self.__endpoint = endpoint
        from .msgloader import HttpMessageLoader
        self._messages = HttpMessageLoader(action=self)

    @property
    def name(self):
        return self.__name

    @property
    def message(self):
        return self._messages

    @property
    def _endpoint(self):
        return self.__endpoint

    def send(self, msg_name=None, **fargs) -> HttpResponse:
        return self.message.send(msg_name, **fargs)

    def perform(self, **fargs) -> HttpResponse:
        pass

class AnonEndPointAction(BaseHttpEndPointAction):

    def __init__(self, *, endpoint):
        super().__init__(name="anon", endpoint=endpoint)

    def perform(self, **fargs):
        pass

class HttpEndPointAction(BaseHttpEndPointAction):

    def __init__(self, *, name, endpoint, **fargs):
        super().__init__(name=name, endpoint=endpoint)
        self.__fargs = fargs
        # Process Yaml file
        from arjuna import C, Yaml
        self.__action_file_path = os.path.join(endpoint.root_dir, "action", name + ".yaml")
        try:
            f = open(self.__action_file_path, "r")
        except FileNotFoundError:
            raise SEAMfulActionFileError(self, msg=f"Message file not found at location: {self.__action_file_path}")
        self.__msg_yaml = f.read()
        f.close()
        self.__store = CIStringDict()

    @property
    def store(self):
        '''
        Values extracted from response and stored.
        '''
        return self.__store

    def _load(self, **sfargs):
        from arjuna import C, Yaml
        margs = {}
        margs.update(self.__fargs)
        margs.update(sfargs)
        from arjuna.core.fmt import arj_format_str, arj_convert
        margs = {k:arj_convert(v) for k,v in margs.items()}
        action_yaml = arj_format_str(self.__msg_yaml, tuple(), margs)
        action_yaml = Yaml.from_str(action_yaml, allow_any=True)
        if action_yaml is None:
            return CIStringDict(), margs, list()

        if "load" in action_yaml:
            from arjuna import Random
            for name, instruction in action_yaml["load"].items():
                if "generator" in instruction:
                    d = {}
                    d.update(instruction)
                    gen = d["generator"]
                    del d["generator"]
                    self.store[name] = getattr(Random, gen)(**d)
                elif "entity" in instruction:
                    mod_path = ".".join([C("project.name"), "lib.entity"])
                    d = {}
                    d.update(instruction)
                    entity = d["entity"]
                    del d["entity"]
                    try:
                        mod = importlib.import_module(mod_path)
                    except ImportError:
                        raise SEAMfulActionFileError(self, f"{mod_path} is not importable. Entity >>{entity}<< can not be loaded. Validate action file: {self.__action_file_path}")
                    else:
                        self.store[name] = getattr(mod, entity)(**d)                    

        if "store" in action_yaml:
            for k, v in action_yaml["store"].items():
                if v in self.store:
                    self.store[k] = self.store[v]
                elif v.split(".")[0] in self.store:
                    ename, attr = v.split(".", 1) 
                    if isinstance(self.store[ename], _DataEntity):
                        self.store[k] = getattr(self.store[ename], attr)
                else:
                    self.store[k] = v
        
        margs.update(self.store)
        

        mproc = None
        if "messages" in action_yaml:
            mproc = _HttpActionSteps(self, action_yaml['messages'])
            del action_yaml["messages"]
        else:
            mproc = _HttpActionSteps(self)
        
        return CIStringDict(), margs, mproc

    def perform(self, **fargs):
        meta, fargs, steps = self._load(**fargs)
        for step in steps:
            response = step.perform(**fargs)
            self.store.update(response.store)
