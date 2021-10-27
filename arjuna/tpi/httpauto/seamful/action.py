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

from arjuna.tpi.parser.yaml import YamlDict
from arjuna.tpi.data.generator import generator
import os

from arjuna.tpi.httpauto.response import HttpResponse
from arjuna.tpi.error import SEAMfulActionFileError
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.tpi.data.entity import _DataEntity
from arjuna import Random
from arjuna.tpi.helper.arjtype import NotFound
from arjuna.tpi.parser.text import Text

def check_data_arg_type(kwargs):
    if 'data' in kwargs:
        if type(kwargs['data']) is not dict and not isinstance(kwargs['data'], _DataEntity):
            raise Exception("'data' keyword argument for action call or action.perform() call can only be a Python dict or an Arjuna Data Entity. Provided: >>{}<< of type >>{}<<".format(kwargs['data'], type(kwargs['data'])))


class _HttpActionStep:

    def __init__(self, action, step_yaml):
        self.__action = action
        self.__msg = step_yaml

    @property
    def _message(self):
        return self.__msg

    def perform(self, **fargs):
        return self.__action.send(self.__msg, **fargs)

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
    def _message(self):
        return self._messages

    @property
    def _endpoint(self):
        return self.__endpoint

    def send(self, msg=None, **fargs) -> HttpResponse:
        check_data_arg_type(fargs)
        return self._message.send(msg, **fargs)

    def perform(self, **fargs) -> HttpResponse:
        pass

    def _get_file_path_msg(self):
        return ""

    def __str__(self):
        meta_str = f"HTTP Action: >{self.name}<" + self._get_file_path_msg()
        if self._endpoint.name != "anon":
            meta_str += f" for end point >{self._endpoint.name}<"
        if self._endpoint.service.name != "anon":
            meta_str += f" for service >{self._endpoint.service.name}<"
        return meta_str

    __repr__ = __str__

class AnonEndPointAction(BaseHttpEndPointAction):

    def __init__(self, *, endpoint):
        super().__init__(name="anon", endpoint=endpoint)

    def perform(self, **fargs):
        pass

class HttpMessageResponse:

    def __init__(self, *, step, msg, response):
        self.__step = step
        self.__msg = msg
        self.__response = response

    @property
    def step(self):
        '''
            Step number for message in the action starting from 1.
        '''
        return self.__step

    @property
    def msg(self):
        '''
           HTTP Message name.
        '''
        return self.__msg

    @property
    def response(self):
        '''
            HTTP Response object.
        '''
        return self.__response

    def __str__(self):
        return str({
            "step": self.step,
            "msg": self.msg,
            "response": self.response
        })

    __repr__ = __str__

class HttpEndPointAction(BaseHttpEndPointAction):

    def __init__(self, *, name, endpoint, **fargs):
        super().__init__(name=name, endpoint=endpoint)
        check_data_arg_type(fargs)
        self.__fargs = fargs
        # Process Yaml file
        from arjuna import C, Yaml
        # Check Built-In Security Action
        my_dir = os.path.dirname(os.path.realpath(__file__))
        self.__action_file_path = os.path.abspath(os.path.join(my_dir, "..", "..","..", "res", "security", "http", "action", name + ".yaml"))
        try:
            f = open(self.__action_file_path, "r")
        except FileNotFoundError:
            self.__action_file_path = os.path.join(endpoint.root_dir, "action", name + ".yaml")
            try:
                f = open(self.__action_file_path, "r")
            except FileNotFoundError:
                raise SEAMfulActionFileError(self, msg=f"Action file not found at location: {self.__action_file_path}")
        self.__msg_yaml = f.read()
        f.close()
        self.__store = CIStringDict()

    def _get_file_path_msg(self):
        return f" at ({self.__action_file_path})"

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
        from arjuna.core.fmt import arj_convert
        margs = {k:arj_convert(v) for k,v in margs.items()}
        action_yaml = Text(self.__msg_yaml).format(**margs)
        action_yaml = Yaml.from_str(action_yaml, allow_any=True)
        if action_yaml is None:
            return CIStringDict(), margs, list()

        def call_generator(in_dict):
            d = {}
            d.update(in_dict)
            gen = d["generator"]
            del d["generator"]
            return getattr(Random, gen)(**d)       

        def gen_or_value(value):
            if isinstance(value, YamlDict):
                if "generator" in value:
                    return call_generator(value)
                else:
                    return value
            else:
                return value

        if 'data' not in self.store:
            self.store['data'] = CIStringDict()

        if "data" in action_yaml:
            for name, instruction in action_yaml["data"].items():
                if type(instruction) is dict or isinstance(instruction, YamlDict):
                    if "generator" in instruction:
                        self.store['data'][name] = call_generator(instruction)
                    else:
                        self.store['data'][name] = instruction
            
        if "entity" in action_yaml:
            from arjuna.core.importer import import_arj_entity
            for name, instruction in action_yaml["entity"].items():
                if name == "data":
                    raise SEAMfulActionFileError(self, msg=f"Entity name can not be >>data<< as it is reserved space for action.store.data. Validate action file: {self.__action_file_path}")                 
                if type(instruction) is str:
                    entity = instruction
                    kwargs = {}
                elif type(instruction) is dict or isinstance(instruction, YamlDict):
                    entity = instruction['type']
                    kwargs = {}
                    kwargs.update(instruction.items())
                    del kwargs['type']
                else:
                    raise SEAMfulActionFileError(self, msg=f"Entity >>{entity}<< can not be loaded. Its value can either be the Entity Class Name or dictionary has 'type' key set to Entity Class Name and rest of them are keyword arguments. Validate action file: {self.__action_file_path}")                 
                try:
                    entity_callable = import_arj_entity(entity)
                except Exception as e:
                    raise SEAMfulActionFileError(self, msg=f"Entity >>{entity}<< can not be loaded. Error: {e}. Validate action file: {self.__action_file_path}")                 
                else:
                    entity_kwarg_dict = {k:gen_or_value(v) for k,v in kwargs.items()}
                    self.store[name] = entity_callable(**entity_kwarg_dict)

        if "alias" in action_yaml:
            for k, v in action_yaml["alias"].items():
                if v in self.store:
                    self.store[k] = self.store[v]
                elif v in self.store['data']:
                    self.store[k] = self.store['data'][v]
                elif v.split(".")[0] in self.store:
                    ename, attr = v.split(".", 1) 
                    if isinstance(self.store[ename], _DataEntity):
                        self.store[k] = getattr(self.store[ename], attr)
                else:
                    self.store[k] = v
        
        if 'data' in margs:
            if isinstance(margs['data'], _DataEntity):
                margs['data'] = margs['data'].as_dict()
        else:
            margs['data'] = dict()
        margs['data'].update(self.store['data'])

        margs.update({k:v for k,v in self.store.items() if k != "data"})

        mproc = None
        if "messages" in action_yaml:
            mproc = _HttpActionSteps(self, action_yaml['messages'])
            del action_yaml["messages"]
        else:
            mproc = _HttpActionSteps(self)
        
        return CIStringDict(), margs, mproc

    def perform(self, **fargs):
        from arjuna import log_info
        log_info(f"Performing", self)
        check_data_arg_type(fargs)
        responses = list()
        meta, fargs, steps = self._load(**fargs)
        for index, step in enumerate(steps):
            response = step.perform(**fargs)
            new_data = {k:v for k,v in response.store.items() if k != "default_content" and not isinstance(v, NotFound)}
            self.store.update(new_data)
            fargs.update(new_data)
            responses.append(HttpMessageResponse(step=index+1, msg=step._message, response=response))
        return responses
