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

from arjuna.tpi.enums import ArjunaOption
from arjuna.unitee.test.objects.fixture import Fixture
from arjuna.unitee.enums import FixtureTypeEnum
from arjuna.unitee.loader import kfactory
from arjuna.unitee.enums import *

class _FixtureDef:
    def __init__(self, ftype, fix_func):
        self.__func = fix_func
        self.__type = ftype

    @property
    def name(self):
        return self.__func.name

    @property
    def func(self):
        return self.__func.obj

    @property
    def qname(self):
        return self.__func.qname

    @property
    def type(self):
        return self.__type

    def create_fixture(self):
        return Fixture(self)

class FixturesDef:
    def __init__(self):
        self.__fixtures = {
            FixtureTypeEnum.INIT_SESSION : None,
            FixtureTypeEnum.END_SESSION : None,
            FixtureTypeEnum.INIT_EACH_STAGE : None,
            FixtureTypeEnum.END_EACH_STAGE : None,
            FixtureTypeEnum.INIT_STAGE : None,
            FixtureTypeEnum.END_STAGE : None,
            FixtureTypeEnum.INIT_EACH_GROUP : None,
            FixtureTypeEnum.END_EACH_GROUP : None,
            FixtureTypeEnum.INIT_GROUP : None,
            FixtureTypeEnum.END_GROUP : None,
            FixtureTypeEnum.INIT_EACH_MODULE : None,
            FixtureTypeEnum.END_EACH_MODULE : None,
            FixtureTypeEnum.INIT_MODULE: None,
            FixtureTypeEnum.END_MODULE: None,
            FixtureTypeEnum.INIT_EACH_FUNCTION: None,
            FixtureTypeEnum.END_EACH_FUNCTION: None,
            FixtureTypeEnum.INIT_EACH_TEST: None,
            FixtureTypeEnum.END_EACH_TEST: None
        }

    def add_fixture_func(self, f_type, f_func):
        self.__fixtures[f_type] = _FixtureDef(f_type, f_func)

    def build(self, f_type):
        if self.__fixtures[f_type]:
            return self.__fixtures[f_type].create_fixture()
        else:
            return None

    def get_fixture_name(self, ftype):
        return self.__fixtures[ftype] and self.__fixtures[ftype].name or None

class ConfiguredFixtureHelper:

    @staticmethod
    def configure_fixture(fixdef, ftypestr, mname, fname):
        from arjuna.tpi import Arjuna
        fix_prefix = Arjuna.get_central_config().get_arjuna_option_value(ArjunaOption.UNITEE_PROJECT_FIXTURES_IMPORT_PREFIX).as_string()
        module = importlib.import_module(fix_prefix + mname)
        func = getattr(module, fname)
        fixdef.add_fixture_func(FixtureTypeEnum[ftypestr.upper()], kfactory.create_fixture(ftypestr, func))