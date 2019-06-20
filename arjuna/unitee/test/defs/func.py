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

from .base import *

from arjuna.unitee.types.containers import *
from arjuna.unitee.test.defs.deps import *
from arjuna.unitee.ddt.source import *

class FuncDef(TestSourceDef):
    def __init__(self, mdef, t):
        super().__init__()
        self.mdef = mdef
        self.pkg = t.pkg
        self.module = t.module
        self.name = t.name
        self.qname = t.qname

        self.func = t.obj
        self.__threads = 1

        self.tvars = TestVars()
        self.tvars.info.function = FunctionInfo()
        self.tvars.info.function.meta['name'] = self.name
        self.tvars.info.function.meta['qname'] = self.qname

        self.__dependency = None
        self.__data_driver = None

    @property
    def threads(self):
        return self.__threads

    @threads.setter
    def threads(self, count):
        self.__threads = count

    def set_evars(self, variables):
        if variables:
            self.tvars.evars.update(variables.get_dict())

    @property
    def data_driver(self):
        return self.__data_driver

    @data_driver.setter
    def data_driver(self,data_driver):
        self.__data_driver = data_driver

    @property
    def data_source(self):
        if self.__data_driver:
            return self.__data_driver.build()
        else:
            return DummyDataSource()

    @property
    def dependency(self):
        return self.__dependency

    @dependency.setter
    def dependency(self, dep):
        if not dep: return
        if not isinstance(dep, Dependency):
            raise Exception ("exclude_if attribute expects the value to be a dependency object.")
        elif not dep.is_fdep():
            raise Exception("exclude_if attribute in @test_function expects the dependency object of functions().")
        else:
            self.__dependency = dep

    def enumerate(self):
        self.console.marker(50, 'f')
        self.console.display("Function:", self.name)
        self.console.display(self.tvars)
        self.console.marker(50, 'f')

