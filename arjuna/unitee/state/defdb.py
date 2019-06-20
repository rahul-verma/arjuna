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

from arjuna.unitee.loader.deptree import DepTreeBuilder

class DefDB:
    def __init__(self):
        self.__dep_tree_builder = DepTreeBuilder()
        # For pulling out class definitions by name
        self.__skipped = []
        self.__unpicked = []

        self.__mdefs = {}
        self.__mqueue = []
        # The following gets populated from above, if classDef.isNotPickedByAnyGroup() is True
        self.__for_processor = []
        from arjuna.tpi import Arjuna
        self.logger = Arjuna.get_logger()

    def register_mdef(self, mdef):
        qname = mdef.qname
        self.logger.debug("Registering method definition for: {}".format(qname))
        self.__mdefs[qname] = mdef
        self.__mqueue.append(qname)

    def freeze(self):
        self.__iter = iter(self.__mdefs)

    def get_mnames(self):
        return self.__mqueue

    def get_mdef(self, mname):
        return self.__mdefs[mname]

    def __iter__(self):
        return iter(self.__mdefs.items())

    def __should_include(self, fname, unpicked_set, skip_set):
        if fname in unpicked_set:
            return False
        if fname in skip_set:
            return False
        return True

    def process_unpicked_and_skipped(self):
        temp1 = set()
        temp2 = set()
        for mname, mdef in self:
            if mdef.unpicked:
                self.__unpicked.append((mdef.pkg, mdef.module))
                temp1.add(mname)
            elif mdef.skipped:
                self.__skipped.append((mdef.pkg, mdef.module))
                temp2.add(mname)
            else:
                mdef.process_unpicked_and_skipped()
        self.__mdefs = {i:j for i,j in self.__mdefs.items() if self.__should_include(i, temp1, temp2)}
        self.__mqueue = [i for i in self.__mqueue if i in self.__mdefs]

    def process_dependencies(self):
        for name in self.__mqueue:
            mdef = self.__mdefs[name]
            mdef.process_dependencies()
            if mdef.dependency:
                mdef.dependency.process()
                for du in mdef.dependency:
                    if du.name not in self.__mdefs:
                        du.set_ignored()
            self.__dep_tree_builder.create_node(name, mdef.dependency)

        self.__dep_tree_builder.process_dependencies()
        self.__dep_tree_builder.validate()


    def slot_module_names(self, module_names):
        return self.__dep_tree_builder.slot_names(module_names)

    def get_mdef_queue_for_def_processor(self):
        return self.__for_processor


    def get_tsclass_definition(name):
        return test_class_definitions[name]

    def get_dependency_tree_builder(self):
        return self.__dep_tree_builder


    def is_test_class(self, name):
        return name in self._mdefs


    def is_test_class_marked_as_skipped(self, name):
        if not is_test_class(name):
            raise Exception("Not a test class")
        else:
            return self._mdefs[name].skipped


    def has_class(self, name):
        return name in self.__all_class_name_set


    def should_run_module(self, qname):
        return qname in self.__mqueue