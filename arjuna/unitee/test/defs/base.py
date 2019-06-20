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

from arjuna.unitee.enums import *
from arjuna.lib.types.descriptors import *
class TestSourceDef:
    def __init__(self):
        self.pkg = None
        self.module = None
        self.func = None
        self.qname = None

        self.__tvars = None
        self.__threads = None
        self.__deps = None
        self.__drefs = None
        self.__dsources = []
        self.__instances = []

        self.__skipped = False
        self.__skip_code = None
        self.selected = False
        self.__unpicked = True
        self.__unpick_code = None

        self.consumed = False

        from arjuna.tpi import Arjuna
        self.console = Arjuna.get_console()
        self.logger = Arjuna.get_logger()
        self.central_config = Arjuna.get_central_config()

    @property
    def tvars(self):
        return self.__tvars

    @tvars.setter
    def tvars(self, tvars):
        self.__tvars = tvars

    @property
    def threads(self):
        return self.__threads

    @threads.setter
    def threads(self, threads):
        self.__threads = RangeBoundInt.validate(threads, 1, 100)

    @property
    def deps(self):
        return self.__deps

    @deps.setter
    def deps(self, value):
        self.__threads = value

    @property
    def drefs(self):
        return self.__drefs

    @drefs.setter
    def drefs(self, value):
        self.__threads = value

    @property
    def dsources(self):
        if self.__dsource is None:
            return DataDriver(dklass(DummyDataSource))
        else:
            return DataDriver(self.__dsources)  # Dsources themselves can be data sources or data drivers.

    def add_dsource(self, dsource):
        self.__dsources.append(dsource)

    def prepend_dsource(self, dsource):
        self._dsources.insert(0, dsource)

    @property
    def skipped(self):
        return self.__skipped

    @skipped.setter
    def skipped(self, flag):
        self.__skipped = flag

    @property
    def skip_code(self):
        return self.__skip_code

    def set_skip_code(self, code):
        self.__skipped = True
        self.__skip_code = code

    @property
    def picked(self):
        return not self.__unpicked

    def set_picked(self):
        self.__unpicked = False
        self.__unpick_code = None

    @property
    def unpicked(self):
        return self.__unpicked

    @unpicked.setter
    def unpicked(self, code):
        self.unpicked = True
        self.__unpick_code = code

    @property
    def unpick_code(self):
        return self.__unpick_code

    @property
    def skip_code(self):
        return self.__skip_code