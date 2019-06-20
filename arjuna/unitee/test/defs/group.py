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

from arjuna.tpi import Arjuna
from arjuna.lib.reader.hocon import *
from arjuna.unitee.types.containers import *
from arjuna.unitee.types.root import *

from arjuna.lib.utils import sys_utils
from arjuna.lib.utils import etree_utils
from arjuna.unitee.utils import run_conf_utils


class GroupDef(Root):

    def __init__(self, sdef, stage_def, id, group_xml_from_session):
        super().__init__()
        self.unitee = Arjuna.get_unitee_instance()
        self.sdef = sdef
        self.stage_def = stage_def
        self.id = id
        self.root = group_xml_from_session
        self.__gconf = None
        self.__iter = None
        self.__process()

        self.__mnames = []
        self.__mod_fname_map = {}

    @property
    def fixture_defs(self):
        return self.__gconf.fixture_defs

    @property
    def rules(self):
        return self.__gconf.rules

    @property
    def threads(self):
        return self.__gconf.threads
        
    def __getattr__(self, item):
        return vars(self.__gconf)[item]

    def __process(self):
        def display_err_and_exit(msg):
            self.console.display_error((msg + " Fix session template file: {}").format(self.sdef.fpath))
            sys_utils.fexit()

        group_attrs = etree_utils.convert_attribs_to_cidict(self.root)
        self.name = group_attrs['name'].strip()
        if not self.name:
            display_err_and_exit(
                ">>name<< attribute in group definition can not be empty.")

        if self.name not in self.unitee.groups:
            display_err_and_exit(
                ">>name<< attribute in group definition is pointing to a non-existing group '{}'.".format(self.name))
        else:
            self.__gconf = self.unitee.groups[self.name]

        threads_err_msg = ">>threads<< attribute in stage definition can be integer >=1."
        if "threads" in group_attrs:
            self.threads = group_attrs['threads'].strip()
            try:
                self.threads = int(self.threads)
            except:
                display_err_and_exit(threads_err_msg)
            else:
                if self.threads <=0:
                    display_err_and_exit(threads_err_msg)

        node_dict = etree_utils.convert_to_cidict(self.root)

        for child_name, child in node_dict.items():
            if child.tag == 'evars':
                evars = child
                for child in evars:
                    run_conf_utils.validate_config_xml_child("session", self.sdef.fpath, child)
                    run_conf_utils.add_config_node_to_configuration("session", self.__gconf.evars, child)
            else:
                display_err_and_exit("Unexpected element >>{}<< found in >>group<< definition in session file.".format(child.tag))

    def pick(self):
        mnames = self.unitee.testdb.get_mnames()

        # Pick what you can
        group_tfunc_count = 0
        for mname in mnames:
            if self.picker.include_module(mname):
                mdef = self.unitee.testdb.get_mdef(mname)
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
        return [mname for mname in self.__mnames if self.unitee.testdb.should_run_module(mname)]

    def get_schedule_module_map(self):
        out_map = {}
        for mqname, fqnames in self.__mod_fname_map.items():
            if self.unitee.testdb.should_run_module(mqname):
                out_map[mqname]= []
                mdef = self.unitee.testdb.get_mdef(mqname);
                for fqname in fqnames:
                    if mdef.should_run_func(fqname):
                        out_map[mqname].append(fqname)
        return out_map