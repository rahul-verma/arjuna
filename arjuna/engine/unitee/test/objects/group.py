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
from .gslot import TestGroupSlot
from arjuna.unitee.engine.pool import TestObjectThreadPool
from arjuna.unitee.enums import *
from arjuna.unitee.state.states import *

class TestGroup(TestObject):
	def __init__(self, num, stage, defn):
		super().__init__(TestObjectTypeEnum.Group)
		self.num = num
		self.stage = stage
		self.defn = defn
		self.rules = self.defn.rules
		self.thcount = 1
		self.mthread_count = self.defn.threads
		self.gslots = []
		self.__module_map = None
		self.state = GroupState()
		self.fixture_defs = self.defn.fixture_defs
		self.append_before_fixture(self.stage.fixture_defs.build(FixtureTypeEnum.INIT_EACH_GROUP))
		self.append_before_fixture(self.fixture_defs.build(FixtureTypeEnum.INIT_GROUP))
		self.append_after_fixture(self.fixture_defs.build(FixtureTypeEnum.END_GROUP))
		self.append_after_fixture(self.stage.fixture_defs.build(FixtureTypeEnum.END_EACH_GROUP))

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)
		picked_mnames = self.defn.get_picked_mnames()

		self.__module_map = self.defn.get_schedule_module_map()
		slots = self.unitee.testdb.slot_module_names(picked_mnames)

		for index, mnames in enumerate(slots):
			gslot = TestGroupSlot(index + 1, self, mnames)
			gslot.load(self.tvars.clone())
			self.gslots.append(gslot)

		self.children = self.gslots

	def _populate_tvars(self, base_tvars):
		self.tvars = base_tvars
		self.tvars.info.group.meta['name'] = self.defn.name
		if not self.defn.config.is_empty():
			self.tvars.context.update_with_file_config_container(self.defn.config)

	def _execute(self):
		tp = TestObjectThreadPool(self.thcount, self, "{}::{}".format(self.thname, "gs"))
		tp.run()

	def get_fnames_for_module(self, mname):
		return self.__module_map[mname]

	def report(self, result):
		super().report(result)
		self.stage.state.update(result)
		self.stage.state.update_test_summary_from_state(self.state)