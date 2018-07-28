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

from arjuna.lib.core.reader.hocon import *
from arjuna.lib.unitee.types.containers import *
from arjuna.lib.unitee.types.root import *

from arjuna.lib.core.utils import sys_utils

from pyhocon import ConfigTree

Unitee = None

class GroupDef(Root):

    def __init__(self, sdef, stage_def, id, group_hocon_from_session_file):
        super().__init__()
        from arjuna.lib.unitee import Unitee as unitee
        global Unitee
        Unitee = unitee
        self.sdef = sdef
        self.stage_def = stage_def
        self.id = id
        self.__gconf = None
        self.__iter = None
        self.__process(group_hocon_from_session_file)

        self.__mnames = []
        self.__mod_fname_map = {}

    @property
    def fixture_defs(self):
        return self.__gconf.fixture_defs

    @property
    def threads(self):
        return self.__gconf.threads
        
    def __getattr__(self, item):
        return vars(self.__gconf)[item]

    def __process(self, group_hocon):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.sdef.fpath))
            sys_utils.fexit()

        if type(group_hocon) is str:
            self.__gconf = self.unitee.groups[group_hocon]
        else:
            r = HoconConfigDictReader(group_hocon)
            r.process()

            gdict = CIStringDict(r.get_map())

            if 'name' not in gdict:
                display_err_and_exit(">>name<< attribute must be specified in group description dict.")
            else:
                conf = gdict['name']
                ctype = type(conf)
                if ctype is not str or not conf:
                    display_err_and_exit(">>name<< attribute in group definition should be a non-empty string.")
                elif conf not in Unitee.groups:
                    display_err_and_exit(">>name<< attribute in group definition is pointing to a non-existing group '{}'.".format(conf))
                else:
                    self.__gconf = Unitee.groups[conf]
                    del gdict['name']

            for cname, conf in gdict.items():
                ctype = type(conf)
                if cname == 'evars':
                    if ctype is not ConfigTree:
                        display_err_and_exit(">>evars<< attribute in group definition should be a dict.")
                    else:
                        self.__gconf.evars.update(conf)
                elif cname == "threads":
                    if ctype is not int and conf <= 1:
                        display_err_and_exit(">>threads<< attribute in group definition can be integer >=1.")
                    else:
                        self.__gconf.threads = conf
                else:
                    display_err_and_exit("Unexpected attribute >>" + cname + "<< found in stage definition.")

    def pick(self):
        mnames = Unitee.testdb.get_mnames()

        # Pick what you can
        group_tfunc_count = 0
        for mname in mnames:
            if self.picker.include_module(mname):
                mdef = Unitee.testdb.get_mdef(mname)
                mdef.set_picked()
                scheduled_fnames = []
                tfunc_count = 0
                for fname in mdef.get_func_names():
                    if self.picker.include_func(fname):
                        fdef = mdef.get_fdef(fname)
                        scheduled_fnames.append(fname)
                        tfunc_count += 1
                        fdef.set_picked()
                    else:
                        continue
                if tfunc_count != 0:
                    self.__mnames.append(mname)
                    self.__mod_fname_map[mname] = scheduled_fnames
                    group_tfunc_count += tfunc_count
            else:
                continue

        return group_tfunc_count

    def get_picked_mnames(self):
        return self.__mnames

    def get_module_map(self):
        return self.__mod_fname_map