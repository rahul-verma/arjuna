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

import re
from arjuna.lib.unitee.enums import *
from arjuna.lib.unitee.types.containers import *
from arjuna.lib.core.reader.hocon import *
from arjuna.lib.core.reader.textfile import *
from arjuna.lib.core.utils import sys_utils
from arjuna.lib.unitee.types.root import *
from arjuna.lib.unitee.test.defs.fixture import *

from pyhocon import ConfigTree

class Picker:

    def __init__(self, fpath, gname, rule_dict):
        self.gname = gname
        self.fpath = fpath
        self._rule_dict = CIStringDict(
            {
                'cm' : [],
                'im' : [],
                'cf' : [],
                'if' : []
            }
        )

        for k,v in rule_dict.items():
            if v is not None:
                try:
                    if type(v) is str:
                        self._rule_dict[k].append(re.compile(v))
                    else:
                        for r in v:
                            self._rule_dict[k].append(re.compile(r))
                except:
                    from arjuna.lib.core import ArjunaCore
                    ArjunaCore.console.display_error("{} group's picker uses invalid regexes. Fix group definitionfile: {}".format(self.gname, self.fpath))
                    sys_utils.fexit()

    def include_module(self, mname):
        if self._rule_dict['cm']:
            consider = False
            for reg in self._rule_dict['cm']:
                if reg.match(mname):
                    consider = True
            return consider

        if self._rule_dict['im']:
            consider = True
            for reg in self._rule_dict['im']:
                if reg.match(mname):
                    consider = False
            return consider

        return True

    def include_func(self, fname):

        if self._rule_dict['cf']:
            consider = False
            for reg in self._rule_dict['cf']:
                if reg.match(fname):
                    consider = True
            return consider

        if self._rule_dict['if']:
            consider = True
            for reg in self._rule_dict['if']:
                if reg.match(fname):
                    consider = False
            return consider

        return True

class PickerFactory:

    def create_picker(gname, pdict, pfpath):
        def display_err_and_exit(msg):
            from arjuna.lib.core import ArjunaCore
            ArjunaCore.console.display_error((msg + " Fix pickers file: {}").format(pfpath))
            sys_utils.fexit()

        rule_found = False
        allowed_types = {str,list}
        allowed_names = {i.lower() for i in PickerRuleEnum.__members__}

        for cname, conf in pdict.items():
            ctype = type(conf)
            if cname not in allowed_names:
                display_err_and_exit("Unexpected attribute >>" + cname + "<< found in picker definition.")
            elif ctype not in allowed_types:
                display_err_and_exit(">>{}<< attribute in picker definition should be a string or list of strings.".format(cname))
            else:
                if ctype is list:
                    for i in conf:
                        if type(i) is not str:
                            display_err_and_exit(">>{}<< list values in picker definition should be strings.".format(cname))

        return Picker(pfpath, gname, pdict)

class GroupConf(Root):

    def __init__(self, name, gconf_dict, fpath):
        super().__init__()
        self.name = name
        self.evars = SingleObjectVars()
        self.picker = None
        self.threads = 1
        self.fpath = fpath
        self.__fixtures = FixturesDef()
        self.__process(gconf_dict)

    @property
    def fixture_defs(self):
        return self.__fixtures

    def __process(self, gdict):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix group template file: {}").format(self.fpath))
            sys_utils.fexit()

        if 'picker' not in gdict:
            display_err_and_exit(">>picker<< attribute must be specified in group description dict.")

        for cname, conf in gdict.items():
            ctype = type(conf)
            if cname == 'evars':
                if ctype is not ConfigTree:
                    display_err_and_exit(">>evars<< attribute in group definition should be a dict.")
                else:
                    self.evars.update(conf)
            elif cname == "threads":
                if ctype is not int and conf <= 1:
                    display_err_and_exit(">>threads<< attribute in group definition can be integer >=1.")
                else:
                    self.threads = conf
            elif cname == "picker":
                if not isinstance(conf, dict) or not conf:
                    display_err_and_exit(">>picker<< attribute in group definition should be a non-empty dict.")
                else:
                    from arjuna.lib.unitee import UniteeFacade
                    pr = HoconConfigDictReader(conf)
                    pr.process()
                    pdict = CIStringDict(pr.get_map())
                    self.picker = PickerFactory.create_picker(self.name, pdict, self.fpath)
            elif cname in {"init_group", "end_group", "init_each_module", "end_each_module"}:
                if ctype is not str or not conf:
                    display_err_and_exit(">>{}<< attribute in session definition should be a non-empty string.".format(cname))
                else:
                    ConfiguredFixtureHelper.configure_fixture(self.__fixtures, cname, conf)
            else:
                display_err_and_exit("Unexpected attribute >>" + cname + "<< found in stage definition.")

class GroupConfsLoader:

    def __load_pick_all(gconfs):
        gconfs['_magroup'] = GroupConf('_magroup', {
                                                        'picker' : {'cm' : [".*"]}
                                                    },
                                        "--builtin--"
                            )

    def __load_user_gconfs(gconfs):
        from arjuna.lib.core import ArjunaCore
        ugcdir = ArjunaCore.config.value(UniteePropertyEnum.PROJECT_CONFIG_DIR)
        ugfpath = os.path.join(ugcdir, "groups.conf")
        ugreader = HoconFileReader(ugfpath)
        ugreader.process()
        ugconfs = ugreader.get_map()
        for k, ghocon in ugconfs.items():
            r = HoconConfigDictReader(ghocon)
            r.process()
            gdict = CIStringDict(r.get_map())
            gconfs[k] = GroupConf(k, gdict, ugfpath)

    def load():
        gconfs = CIStringDict()
        GroupConfsLoader.__load_pick_all(gconfs)
        GroupConfsLoader.__load_user_gconfs(gconfs)
        return gconfs



