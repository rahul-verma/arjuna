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

from arjuna.lib.unitee.types.root import *
from arjuna.lib.unitee.types.containers import *
from arjuna.lib.core.reader.hocon import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.unitee.test.defs.fixture import *

from .group import *

from pyhocon import ConfigTree

class StageDef(Root):
    def __init__(self, sdef, id, stage_hocon):
        super().__init__()
        self.gdefs = []
        self.tmcount = 0
        self.threads = 1
        self.evars = SingleObjectVars()
        self.sdef = sdef
        self.__iter = None
        self.__fixtures = FixturesDef()

        from arjuna.lib.unitee import UniteeFacade
        self.unitee = UniteeFacade

        self.id = id
        self.name = "stage{:d}".format(id)
        self.evars.update(sdef.evars)

        if not isinstance(stage_hocon, ConfigTree):
            self.console.display_error("Fatal: [Arjuna Error] Unsuppored input argument supplied for stage creation: {}".format(stage_hocon))
            sys_utils.fexit()
        else:
            self.__process(stage_hocon)
            # self.nodes.append(SessionSubNode(self, len(self.nodes) + 1, input))

    @property
    def fixture_defs(self):
        return self.__fixtures

    def __process(self, group_hocon):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.sdef.fpath))
            sys_utils.fexit()

        r = HoconConfigDictReader(group_hocon)
        r.process()

        node_dict = CIStringDict(r.get_map())
        for cname, conf in node_dict.items():
            ctype = type(conf)
            if cname == 'evars':
                if ctype is not ConfigTree:
                    display_err_and_exit(">>execVars<< attribute in stage definition should be a dict.")
                else:
                    self.evars.update(conf)
            elif cname == 'name':
                if ctype is not str or not conf:
                    display_err_and_exit(">>name<< attribute in stage definition should be a non-empty string.")
                else:
                    self.name = conf
            elif cname == "threads":
                if ctype is not int and conf <= 1:
                    display_err_and_exit(">>threads<< attribute in stage definition can be integer >=1.")
                else:
                    self.threads = conf
            elif cname == "groups":
                if ctype is not list or not conf:
                    display_err_and_exit(">>groups<< attribute in stage definition must be a non-empty list.")
                else:
                    for gconf in conf:
                        if type(gconf) in {str, ConfigTree}:
                            self.gdefs.append(GroupDef(self.sdef, self, len(self.gdefs) + 1, gconf))
                        else:
                            display_err_and_exit(">>groups<< attribute in stage can only contain group description dictionaries or names of groups.")
            elif cname in {"init_stage", "end_stage", "init_each_group", "end_each_group"}:
                if ctype is not str or not conf:
                    display_err_and_exit(">>{}<< attribute in session definition should be a non-empty string.".format(cname))
                else:
                    ConfiguredFixtureHelper.configure_fixture(self.fixture_defs, cname, conf)
            else:
                display_err_and_exit("Unexpected attribute >>" + cname + "<< found in stage definition.")

    def pick(self):
        for gdef in self.gdefs:
            self.tmcount += gdef.pick()

        self.__iter = iter(self.gdefs)