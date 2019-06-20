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

from arjuna.lib.thread.decorators import *
from arjuna.unitee.types.containers import *
from arjuna.unitee.test.defs.deps import *
from arjuna.unitee.test.defs.fixture import *
from arjuna.lib.utils import sys_utils
from arjuna.unitee.loader.deptree import DepTreeBuilder

class ModDef(TestSourceDef):
    def __init__(self, pkg, module, qname):
        super().__init__()
        self.__dep_tree_builder = DepTreeBuilder()
        self.lock = threading.RLock()
        self.pkg = pkg
        self.module = module
        self.qname = qname
        self.__threads = 1
        self.tvars = TestVars()
        self.tvars.info.module = ModuleInfo()
        self.tvars.info.module.meta['pkg'] = self.pkg
        self.tvars.info.module.meta['name'] = self.module
        self.tvars.info.module.meta['qname'] = self.qname

        self.__dependency = None
        self.__fixtures = FixturesDef()

        # For checking whether a method name exists in a given class
        self.fnames = set()
        # For pulling out method definitions by name
        self.__fdefs = {}

        self.__skipped = []
        self.__unpicked = []

        self.__fqueue = []
        # This is what would be got by groups for pickers processing. If a group picks up something, it calls setPicked()
        self.for_picker_processing = []
        # The following gets populated from above, if classDef.isNotPickedByAnyGroup() is True
        self.for_processor = []

    @property
    def threads(self):
        return self.__threads

    @threads.setter
    def threads(self, count):
        self.__threads = count

    @property
    def fixture_defs(self):
        return self.__fixtures

    def set_evars(self, variables):
        if variables:
            self.tvars.evars.update(variables.get_dict())

    @property
    def dependency(self):
        return self.__dependency

    @dependency.setter
    def dependency(self, dep):
        if not dep: return
        if not isinstance(dep, Dependency):
            raise Exception ("exclude_if attribute expects the value to be a dependency object.")
        elif not dep.is_mdep():
            raise Exception("exclude_if attribute in @tmodule expects the dependency object of modules().")
        else:
            self.__dependency = dep

    def process_dependencies(self):
        for name in self.__fqueue:
            fdef = self.__fdefs[name]
            if fdef.dependency:
                fdef.dependency.process()
                for du in fdef.dependency:
                    if du.name not in self.__fdefs:
                        du.set_ignored()
            self.__dep_tree_builder.create_node(name, fdef.dependency)

        self.__dep_tree_builder.process_dependencies()
        self.__dep_tree_builder.validate()


    def slot_func_names(self, names):
        return self.__dep_tree_builder.slot_names(names)

    def add_fixture_func(self, ftype, func):
        self.__fixtures.add_fixture_func(ftype, func)

    def get_fixture_name(self, ftype):
        return self.__fixtures.get_fixture_name(ftype)

    def get_func_names(self):
        return self.__fqueue

    def get_fdef(self, name):
        return self.__fdefs[name]

    def __iter__(self):
        return iter(self.__fdefs.items())

    def __should_include(self, fname, unpicked_set, skip_set):
        if fname in unpicked_set:
            return False
        if fname in skip_set:
            return False
        return True

    def process_unpicked_and_skipped(self):
        temp1 = set()
        for fname, fdef in self:
            if fdef.unpicked:
                self.__unpicked.append((fdef.pkg, fdef.module, fdef.name))
                temp1.add(fdef.name)

        temp2 = set()
        for fname, fdef in self:
            if fdef.skipped:
                self.__skipped.append((fdef.pkg, fdef.module, fdef.name))
                temp2.add(fdef.name)

        self.__fdefs = {i:j for i, j in self.__fdefs.items() if self.__should_include(i, temp1, temp2)}
        self.__fqueue = [i for i in self.__fqueue if i in self.__fdefs]

    def register_fdef(self, fdef):
        name = fdef.name
        self.logger.debug("Registering function definition for: {}".format(name))

        self.fnames.add(name)
        self.__fdefs[name] = fdef
        self.__fqueue.append(name)

    def enumerate(self):
        self.console.marker(50, '+')
        self.console.display(self.tvars)
        self.console.marker(50, '+')
        names = list(self.__fdefs.keys())
        names.sort()
        for name in names:
            fd = self.__fdefs[name]
            fd.enumerate()

    def should_run_func(self, qname):
        return qname in self.__fqueue