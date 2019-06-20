'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import abc
from enum import Enum, auto
from arjuna.lib.utils import obj_utils

class TestObjectsEnum:
    MODULES = auto()
    FUNCTIONS = auto()

class TestObjects:

    def __init__(self, objects, ctype):
        self.__objects = objects
        self.__ctype = ctype

    @property
    def type(self):
        return self.__ctype

    @property
    def objects(self):
        return self.__objects

    def __iter__(self):
        return iter(self.objects)

class modules(TestObjects):

    def __init__(self, module, *modules):
        super().__init__([module] + list(modules), TestObjectsEnum.MODULES)

        for module in self.objects:
            if not obj_utils.is_module(module):
                raise Exception("modules() call expects all arguments to be module objects. {} is not a module".format(module))

class functions(TestObjects):

    def __init__(self, func, *funcs):
        super().__init__([func] + list(funcs), TestObjectsEnum.FUNCTIONS)

        for func in self.objects:
            if not obj_utils.is_function(func):
                raise Exception("functions() call expects all arguments to be function (unbound, non-inner) objects. {} is not a function".format(func))

class DepUnit(metaclass=abc.ABCMeta):

    def __init__(self, name):
        self.__ignore = False
        self.__name = name

    @property
    def name(self):
        return self.__name

    def should_ignore(self):
        return self.__ignore

    def set_ignored(self):
        self.__ignore = True

    @abc.abstractmethod
    def evaluate(self, state):
        pass

class ProblemDepUnit(DepUnit):
    def __init__(self, name):
        super().__init__(name)

    def evaluate(self, state):
        if not self.should_ignore():
            state.raise_on_problem(self.name)

class ProlemModule(ProblemDepUnit):
    def __init__(self, mname):
        super().__init__(mname)

class ProblemFunction(ProblemDepUnit):
    def __init__(self, mname, name):
        super().__init__(name)
        self.mname = mname

class Dependency:

    def __init__(self, target):
        self._target = target
        self._depunits = []

    def is_mdep(self):
        return self._target.type == TestObjectsEnum.MODULES

    def is_fdep(self):
        return self._target.type == TestObjectsEnum.FUNCTIONS

    def append(self, du):
        self._depunits.append(du)

    def __iter__(self):
        return iter(self._depunits)

    def evaluate(self, state):
        for du in self._depunits:
            du.evaluate(state)

class problem_in(Dependency):
    def __init__(self, callables_obj):
        super().__init__(callables_obj)
        if not isinstance(callables_obj, TestObjects):
            raise Exception(
                "problem_in() call expects its argument to be a TestObjects object: either modules() or functions(). Provided: {}".format(
                    callables_obj))
        self._callables = callables_obj

    def process(self):
        klass = None
        if self.is_mdep():
            for obj in self._target:
                self.append(ProlemModule(obj.__name__))
        else:
            for obj in self._target:
                self.append(ProblemFunction(obj.__module__, obj.__name__))
