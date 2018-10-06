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

from arjuna.lib.core.utils import sys_utils
from arjuna.lib.unitee.types.root import Root
from arjuna.lib.unitee.types.containers import *
from arjuna.lib.core.enums import *

from arjuna.lib.core.reader.textfile import *
from arjuna.lib.core.reader.hocon import *
from arjuna.lib.unitee.test.defs.stage import *
from arjuna.lib.unitee.test.objects.session import *
from arjuna.lib.unitee.test.defs.fixture import *

from arjuna.lib.unitee import UniteeFacade

Unitee = UniteeFacade()

class __SessionDef(Root, metaclass=abc.ABCMeta):
    def __init__(self, sname):
        super().__init__()
        self.name = sname
        self.fpath = None
        self.reader = None
        self.stage_defs = []
        self.tmcount = 0
        self.evars = SingleObjectVars()
        self.evars.update(self.central_config.clone_evars())
        self.__iter = None
        self.__fixtures = FixturesDef()

    @property
    def fixture_defs(self):
        return self.__fixtures

    def process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.fpath))
            sys_utils.fexit()

        try:
            self.reader.process()
            sdict = CIStringDict(self.reader.get_map())
        except:
            display_err_and_exit("Session definition could not be loaded because of syntax errors.")

        if 'stages' not in sdict:
            display_err_and_exit(">>stages<< attribute must be specified in session template.")

        for cname, conf in sdict.items():
            cname = cname.lower()
            ctype = type(conf)
            if cname == 'evars':
                if ctype is not ConfigTree:
                    display_err_and_exit(">>evars<< attribute in session definition should be a dict.")
                else:
                    self.evars = conf
            elif cname == "stages":
                if ctype is not list or not conf:
                    display_err_and_exit(">>stages<< attribute in session definition should be a non-empty list.")
                else:
                    for index, entry in enumerate(conf):
                        node = StageDef(self, index + 1, entry)
                        self.stage_defs.append(node)
            elif cname in {"init_session", "end_session", "init_each_stage", "end_each_stage"}:
                if ctype is not str or not conf:
                    display_err_and_exit(">>{}<< attribute in session definition should be a non-empty string.".format(cname))
                else:
                    ConfiguredFixtureHelper.configure_fixture(self.fixture_defs, cname, conf)
            else:
                display_err_and_exit("Unexpected attribute {}:{} found in session definition.".format(cname, conf))

    def schedule(self):
        logger.debug("%s: Scheduling nodes".format(self.name))
        for stage in self.stage_defs:
            logger.debug("Session node: " + node.get_name())
            stage.schedule()
            self.tmcount += stage.get_tmcount()
        self.__iter = iter(self.stage_defs)

    def pick(self):
        for stage_def in self.stage_defs:
            stage_def.pick()
        Unitee.testdb.process_unpicked_and_skipped()
        Unitee.testdb.process_dependencies()

        return TestSession(self)

class __MSessionDef(__SessionDef):
    def __init__(self, gname):
        super().__init__("msession")
        sr = TextResourceReader("st/msession.conf")
        contents = sr.read()
        sr.close()
        contents = contents.format(gname=gname)
        self.fpath = os.path.join(self.central_config.value(CorePropertyTypeEnum.ARJUNA_ROOT_DIR),
                                  "arjuna/lib/res/st/msession.conf")
        self.reader = HoconStringReader(contents)

class MSessionAllTests(__MSessionDef):
    def __init__(self):
        super().__init__("_magroup")

class MSessionSingleGroup(__MSessionDef):
    def __init__(self, group_name):
        super().__init__(group_name)

class UserDefinedSessionDef(__SessionDef):
    def __init__(self, name, fpath):
        super().__init__(name)
        self.fpath = fpath
        self.reader = HoconFileReader(fpath)
