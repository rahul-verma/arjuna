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

import importlib
from functools import partial
import inspect
import traceback

from arjuna.unitee.test.defs.module import *
from arjuna.unitee.test.defs.func import *
from arjuna.unitee.loader import kfactory
from arjuna.unitee.types.containers import *
from arjuna.unitee.enums import *
from arjuna.unitee.markup import mrules

class ModuleLoader:
    def __init__(self, pkg, module, qname):
        self.pkg = pkg
        self.module = module
        self.qname = qname
        from arjuna.tpi import Arjuna
        self.console = Arjuna.get_console()
        self.logger = Arjuna.get_logger()
        self.mdef = ModDef(pkg, module, qname)
        self._current_kall_ids = {}
        self._current_kall_decs = {}
        self.__multidecs = {}
        from arjuna.tpi import Arjuna
        self.unitee = Arjuna.get_unitee_instance()

    def load(self):
        try:
            self.logger.debug("Importing Module in tests directory: {}".format(self.qname))
            importlib.import_module(self.qname)
        except Exception as e:
            self.console.display_error(
                "Not able to import module: {}. Fix the errors leading to following exception.".format(self.qname))
            self.console.display_exception_block(e, traceback.format_exc())
            sys_utils.fexit()

        self.unitee.testdb.register_mdef(self.mdef)

    def __str(self, obj):
        try:
            return ".".join([obj.__module__, obj.__qualname__])
        except:
            return str(obj)

    def __add_to_multi_dec(self, kallable, dec_name):
        qname = kallable.__qualname__
        if qname not in self.__multidecs:
            self.__multidecs[qname] = []
        self.__multidecs[qname].append(dec_name)

    def __isfunc(self, dtype, dec_name, obj):
        if not obj_utils.is_function(obj):
            self.console.display_error("{} can only be an unbound functions. You have decorated {} with @{}".format(
                dtype,
                self.__str(obj),
                dec_name
            )
            )
            sys_utils.fexit()

    def __isinit(self, dtype, dec_name, obj):
        if obj.__name__ != "__init__":
            self.console.display_error(
                "@tmodule can be used only on a function with name __init__. You have decorated {} with @{}".format(
                    self.__str(obj),
                    dec_name
                )
            )
            sys_utils.fexit()

    def __isnotinit(self, dtype, dec_name, obj):
        if obj.__name__ == "__init__":
            self.console.display_error(
                "__init__ is a reserved function name to initialize the module with @tmodule. You have decorated {} with @{}".format(
                    self.__str(obj),
                    dec_name
                )
            )
            sys_utils.fexit()

    def __ispublic(self, dtype, dec_name, obj):
        if not obj_utils.is_public(obj):
            self.console.display_error(
                "{} should be named as per public convention. Its name can not start with _ and __. You have decorated {} with @{}".format(
                    dtype,
                    self.__str(obj),
                    dec_name
                )
            )
            sys_utils.fexit()

    def __ismysig(self, dtype, dec_name, obj):
        if not obj_utils.is_my_sig(obj):
            msg = "The signature of {} should be def funcname(my). You have decorated {} with @{}"
            msg += "The signature of your function is {}. Correct and proceed."
            self.console.display_error(msg.format(dtype, self.__str(obj), dec_name, inspect.getfullargspec(obj)))
            sys_utils.fexit()

    def __wrongmultientry(self, mqname, fname, dstr):
        msg = "Fatal Error: Unsupported multi-decoration in module {}."
        msg += "{} has been decorated with {}."
        self.console.display_error(msg.format(mqname, fname, dstr))
        sys_utils.fexit()

    def __duplicatefunc(self, mqname, fname, dstr):
        msg = "Fatal Error: Duplicate decorate function names found in module: {}."
        msg += "So far, two separate definitions of function {} were found decorated with {}."
        self.console.display_error(msg.format(mqname, fname, dstr))
        sys_utils.fexit()

    def __validate(self, vfuncs, dtype, dec_name, obj):
        for vfunc in vfuncs:
            vfunc(dtype, dec_name, obj)

    def __register_dec(self, dtype, dec_name, kallable, *, initcheck, fnoentry, fmultidec):
        initcheck(dtype, dec_name, kallable)
        kqname = kallable.__qualname__
        id_dict = self._current_kall_ids
        if kqname in id_dict:
            dstr = ", ".join(["@{}".format(d) for d in ([dec_name] + self._current_kall_decs[kqname])])
            if id(kallable) == id_dict[kqname]:
                self.logger.debug("Multi-decorator situation: {} {} {} {} {}".format(dtype, dec_name, kallable, id(kallable), id_dict[kqname]))
                fmultidec(kallable.__module__, kallable.__qualname__, dstr)
            else:
                self.logger.fatal("Duplicate name problem: {} {} {} {} {}".format(dtype, dec_name, kallable, id(kallable), id_dict[kqname]))
                self.__duplicatefunc(kallable.__module__, kallable.__qualname__, dstr)
        else:
            self.logger.debug("First decorator: {} {} {} {}".format(dtype, dec_name, kallable, id(kallable)))
            fnoentry()
        return kallable

    def __update_tracking(self, kallable, dec_name):
        kqname = kallable.__qualname__
        id_dict = self._current_kall_ids
        dec_dict = self._current_kall_decs
        id_dict[kqname] = id(kallable)
        if kqname not in dec_dict:
            dec_dict[kqname] = []
        dec_dict[kqname].append(dec_name)

    def register_tmodule(self, kallable, **tsargs):
        self.register_fixture("init_module", kallable)

        self.mdef.threads = tsargs['threads']
        del tsargs['threads']
        self.mdef.set_evars(tsargs['evars'])
        del tsargs['evars']
        if tsargs['tags']:
            self.mdef.tvars.tags = tsargs['tags']
        del tsargs['tags']
        if tsargs['bugs']:
            self.mdef.tvars.bugs = tsargs['bugs']
        del tsargs['bugs']
        self.mdef.drive_with = tsargs['drive_with']
        del tsargs['drive_with']
        self.mdef.dependency = tsargs['exclude_if']
        del tsargs['exclude_if']

        # Validate props
        try:
            mrules.validate_built_in_props(tsargs)
        except Exception as e:
            raise Exception("Error in @init_module decorator on function: {}.{}. {}.".format(self.qname,kallable, e))
        self.mdef.tvars.info.module.set_props(tsargs)

    def register_tfunc(self, kallable, **tsargs):
        def register_tfunc():
            self.__update_tracking(kallable, "test_function")
            t = kfactory.create_test_func(kallable)
            td = FuncDef(self.mdef, t)

            td.threads = tsargs['threads']
            del tsargs['threads']
            td.set_evars(tsargs['evars'])
            del tsargs['evars']
            if tsargs['tags']:
                td.tvars.tags = tsargs['tags']
            del tsargs['tags']
            if tsargs['bugs']:
                td.tvars.bugs = tsargs['bugs']
            del tsargs['bugs']
            td.data_driver = tsargs['drive_with']
            del tsargs['drive_with']
            td.data_ref = tsargs['data_ref']
            del tsargs['data_ref']
            td.dependency = tsargs['exclude_if']
            del tsargs['exclude_if']

            # Validate props
            try:
                mrules.validate_built_in_props(tsargs)
            except Exception as e:
                raise Exception("Error in @test decorator of test module: {}. {}.".format(t.qname, e))
            mrules.validate_built_in_props(tsargs)
            td.tvars.info.function.set_props(tsargs)

            self.mdef.register_fdef(td)

        return self.__register_dec(
            "Test function",
            "tfunc",
            kallable,
            initcheck = partial(self.__validate, [self.__isfunc, self.__isnotinit, self.__ispublic, self.__ismysig]),
            fnoentry = register_tfunc,
            fmultidec = self.__wrongmultientry
        )

    def register_fixture(self, dec_name, kallable):
        def register_fixture():
            self.__update_tracking(kallable, dec_name)
            f = kfactory.create_fixture(dec_name, kallable)
            self.mdef.add_fixture_func(f.type, f)

        return self.__register_dec(
            "Fixture function",
            dec_name,
            kallable,
            initcheck= partial(self.__validate, [self.__isfunc, self.__isnotinit, self.__ispublic, self.__ismysig]),
            fnoentry = register_fixture,
            fmultidec = self.__wrongmultientry
        )

    def register_skip(self, kallable):
        def not_a_test():
            msg = "Fatal Error: You have used @skip instruction on a non-test function. "
            msg += "Either @tfunc or @tmodule decorators are missing or have been put in wrong order. "
            msg += "Use @skip\n@tmodule or @skip\@tfunc as applicable."
            self.console.display_error(msg)
            sys_utils.fexit()

        def register_skip(*vargs):
            self.__update_tracking(kallable, "skip")
            if self.mdef.get_fixture_name(FixtureTypeEnum.INIT_MODULE) == kallable.__name__:
                self.mdef.set_skip_code(SkipCodeEnum.SKIP_MODULE_DEC)
            else:
                td = self.mdef.get_fdef(kallable.__qualname__)
                td.set_skip_code(SkipCodeEnum.SKIP_FUNC_DEC)

        return self.__register_dec(
            "Skipped function",
            "skip",
            kallable,
            initcheck = partial(self.__validate, [self.__isfunc, self.__ispublic, self.__ismysig]),
            fnoentry = not_a_test,
            fmultidec = register_skip
        )

    def enumerate(self):
        self.console.display("M" * 50)
        self.console.display("Module: ", self.qname)
        self.mdef.enumerate()
        self.console.display("M" * 50)