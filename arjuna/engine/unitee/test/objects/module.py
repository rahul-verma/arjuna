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
from .mslot import TestModuleSlot
from arjuna.unitee.engine.pool import TestObjectThreadPool
from arjuna.unitee.enums import *
from arjuna.unitee.state.states import *

class TestModule(TestObject):
	def __init__(self, group, mdef):
		super().__init__(TestObjectTypeEnum.Module)
		self.group = group
		self.rules = self.group.rules
		self.defn = mdef
		self.thcount = 1
		self.fthread_count = self.defn.threads
		self.mslots = []
		self.results = {}
		self.fixture_defs = self.defn.fixture_defs
		self.append_before_fixture(self.group.fixture_defs.build(FixtureTypeEnum.INIT_EACH_MODULE))
		self.append_before_fixture(self.fixture_defs.build(FixtureTypeEnum.INIT_MODULE))
		self.append_after_fixture(self.fixture_defs.build(FixtureTypeEnum.END_MODULE))
		self.append_after_fixture(self.group.fixture_defs.build(FixtureTypeEnum.END_EACH_MODULE))

		self.state = ModuleState()
		self.__dependency = self.defn.dependency

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)
		picked_fnames = self.group.get_fnames_for_module(self.defn.qname)

		from arjuna.unitee import Unitee
		slots = self.defn.slot_func_names(picked_fnames)

		for index, slot in enumerate(slots):
			mslot = TestModuleSlot(index + 1, self.group, self, slot)
			mslot.load(self.tvars.clone())
			self.mslots.append(mslot)
		self.children = self.mslots

	def _populate_tvars(self, base_tvars):
		self.tvars = self.defn.tvars.clone()
		self.tvars.context = base_tvars.context
		self.tvars.runtime.update(base_tvars.evars)
		self.tvars.info.session = base_tvars.info.session
		self.tvars.info.stage = base_tvars.info.stage
		self.tvars.info.group = base_tvars.info.group

	def _execute(self):
		tp = TestObjectThreadPool(self.thcount, self, "{}::{}".format(self.thname, "ms"))
		tp.run()

	def report(self, result):
		super().report(result)
		self.group.state.update(result)
		self.group.state.update_test_summary_from_state(self.state)

	def _evaluate_dependency(self):
		if self.__dependency:
			self.__dependency.evaluate(self.group.state)

	def _evaluate_rules(self):
		if self.rules is not None:
			self.rules.evaluate(self)