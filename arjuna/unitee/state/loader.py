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

from arjuna.unitee.loader.mod_loader import *
from arjuna.lib.discovery import *
from arjuna.lib.utils import obj_utils
from arjuna.tpi.enums import ArjunaOption


class TestLoader:
    def __init__(self):
        self.lock = threading.RLock()
        self.__loading_completed = False
        self.__mlmap = {}
        from arjuna.tpi import Arjuna
        central_config = Arjuna.get_central_config()
        self.proj_dir = central_config.get_arjuna_option_value(ArjunaOption.PROJECT_ROOT_DIR).as_string()
        self.test_dir = central_config.get_arjuna_option_value(ArjunaOption.UNITEE_PROJECT_TESTS_DIR).as_string()
        self.logger = Arjuna.get_logger()
        self.console = Arjuna.get_console()

    def load(self):
        self.logger.debug("Now finding tests inside: " + self.proj_dir)
        aggregator = FileAggregator()
        discoverer = FileDiscoverer(aggregator, self.proj_dir, [self.test_dir + "/" + "modules"])
        discoverer.discover()
        aggregator.enumerate()
        for def_file in aggregator:
            file_name = def_file.attr(DiscoveredFileAttributeEnum.FULL_NAME)
            # Arjuna would not import module names that begin with _
            if file_name.startswith("_"): continue
            self.logger.debug("Found: " + def_file.attr(DiscoveredFileAttributeEnum.FULL_NAME))
            self.__handle_discovered_module(def_file)

        ### This STEP needs to be looked into AFTER complete processing is working.
        ###Unitee.def_db.register_with_reporter()

    def __get_pkg_module_qname_for_discovered_file(self, f):
        qname = None
        from arjuna.tpi import Arjuna
        project = Arjuna.get_central_arjuna_option(ArjunaOption.PROJECT_NAME).as_string()
        pkg = ".".join([project, f.attr(DiscoveredFileAttributeEnum.PACKAGE_DOT_NOTATION).strip()])
        module = f.attr(DiscoveredFileAttributeEnum.NAME).strip()
        qname = ".".join([pkg, module])
        return pkg, module, qname

    def __get_pkg_module_qname_from_mqname(self, mqname):
        pkg, module = mqname.rsplit(".", 1)
        qname = mqname
        return pkg, module, mqname

    def __handle_discovered_module(self, def_file):
        pkg, module, qname = self.__get_pkg_module_qname_for_discovered_file(def_file)
        if def_file.attr(DiscoveredFileAttributeEnum.EXTENSION).lower() != "py":
            self.logger.debug("Non-Python file or non-py extension Python file: " + qname)

        if qname not in self.__mlmap:
            self.logger.debug("Loading module: " + qname)
            self.__mlmap[qname] = ModuleLoader(pkg, module, qname)
            self.__mlmap[qname].load()
        else:
            self.logger.debug("Module was already loaded via test script import: " + qname)

        # Here java took an annotation based decision whether it is a test class
        # This should take place now in Module Loader. If @tdmodule is not marked
        # or no tests are present
        # Also, a non-test class should be added by Module Loader to non-test class queue
        # of Unitee.def_db

    def __handle_indirect_imported_module(self, mqname):
        pkg, module, qname = self.__get_pkg_module_qname_from_mqname(mqname)
        self.logger.debug("Loading module: " + qname)
        self.__mlmap[qname] = ModuleLoader(pkg, module, qname)
        self.__mlmap[qname].load()

    def freeze(self):
        self.__loading_completed = True

    def __validate_state(self, kallable, dec_type):
        if self.__loading_completed:
            ktype = type(kallable) is type and "class" or "function"
            from arjuna.tpi import Arjuna
            Arjuna.get_console().display_error(
                "You are decorating inner {} {} with {} in {} module. These decorators are ignored by Arjuna.".format(
                    ktype,
                    kallable.__qualname__,
                    dec_type,
                    kallable.__module__
                ))
            return False
        return True

    def __register(self, dec, what, kallable, *vars, **kwargs):
        proceed = self.__validate_state(kallable, "@{}".format(dec))
        if proceed:
            ml = self.__get_ml(kallable)
            return getattr(ml, "register_" + what)(kallable, *vars, **kwargs)

    def __get_ml(self, kallable):
        if obj_utils.callable(kallable):
            if kallable.__module__ not in self.__mlmap:
                self.__handle_indirect_imported_module(kallable.__module__)
            return self.__mlmap[kallable.__module__]
        else:
            return kallable

    @sync_method('lock')
    def register_tfunc(self, kallable, **tsargs):
        return self.__register("tfunc", "tfunc", kallable, **tsargs)
        # proceed = self.__validate_state(kallable, "@test_source or @ts")
        # if proceed:
        #     ml = self.__get_ml(kallable)
        #     ml.register_tfunc(kallable, **tsargs)
        # return kallable

    @sync_method('lock')
    def register_tmodule(self, kallable, **tsargs):
        proceed = self.__validate_state(kallable, "@test_source or @ts")
        if proceed:
            ml = self.__get_ml(kallable)
            ml.register_tmodule(kallable, **tsargs)
        return kallable

    @sync_method('lock')
    def register_fixture(self, ftype, kallable):
        proceed = self.__validate_state(kallable, "@{}".format(ftype))
        if proceed:
            ml = self.__get_ml(kallable)
            ml.register_fixture(ftype, kallable)
        return kallable

    @sync_method('lock')
    def register_skip_func(self, kallable):
        proceed = self.__validate_state(kallable, "@skip_me")
        if proceed:
            ml = self.__get_ml(kallable)
            ml.register_skip(kallable)
        return kallable

    def enumerate(self):
        names = list(self.__mlmap.keys())
        names.sort()
        for name in names:
            ml = self.__mlmap[name]
            ml.enumerate()