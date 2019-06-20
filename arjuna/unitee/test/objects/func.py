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

from .base import TestObject
from .test import Test
from arjuna.unitee.engine.pool import TestObjectThreadPool
from arjuna.unitee.enums import *
from arjuna.unitee.state.states import *
from arjuna.unitee.reporter.result.types import *
from arjuna.lib.thread import decorators

class TestFunc(TestObject):

	def __init__(self, group, module, mslot, defn):
		super().__init__(TestObjectTypeEnum.Function)
		import threading
		from arjuna.tpi import Arjuna
		self.unitee = Arjuna.get_unitee_instance()
		self.lock = threading.RLock()
		self.group = group
		self.rules = self.group.rules
		self.module = module
		self.mslot = mslot
		self.defn = defn
		self.func_obj = self.defn.func
		self.thcount = self.defn.threads
		self.counter = 0
		self.state = FunctionState()
		self.data_source = None
		self.__dependency = self.defn.dependency
		self.append_before_fixture(self.module.fixture_defs.build(FixtureTypeEnum.INIT_EACH_FUNCTION))
		self.append_after_fixture(self.module.fixture_defs.build(FixtureTypeEnum.END_EACH_FUNCTION))

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)

	@decorators.sync_method('lock')
	def next(self):
		import threading
		try:
			if self.data_source is None:
				self.data_source = self.defn.data_source
		except Exception as e:
			issue = self.unitee.state_mgr.create_issue_from_exception(e, traceback.format_exc(), ResultTypeEnum.ERROR)
			result = TestObjectResult(self, rtype=ResultTypeEnum.ERROR, rcode=ResultCodeEnum.DATASOURCE_CONSTRUCTION_ERROR, iid=issue.iid)
			result.append_issue(issue)
			self.report(result)
			raise SubTestsFinished()

		self.counter += 1
		record = None
		try:
			record = self.data_source.next()
		except DataSourceFinished:
			raise SubTestsFinished()
		else:
			test = Test(self.counter, self.group, self.module, self)
			tvars = self.tvars.clone()
			tvars.data.record = record
			test.load(tvars)
			return test

	def _populate_tvars(self, base_tvars):
		self.tvars = base_tvars
		self.tvars.info.function = self.defn.tvars.info.function
		self.tvars.evars.update(self.defn.tvars.evars)
		self.tvars.tags.update(self.defn.tvars.tags)
		self.tvars.bugs.update(self.defn.tvars.bugs)

	def _execute(self):
		self.tvars.context = self.mslot.tvars.context.clone()
		self.tvars.runtime.update(self.mslot.tvars.runtime)
		tp = TestObjectThreadPool(self.thcount, self, "{}::{}".format(self.thname, "t"))
		tp.run()

	def report(self, result):
		super().report(result)
		self.module.state.update(result)
		self.module.state.update_test_summary_from_state(self.state)

	def _evaluate_dependency(self):
		if self.__dependency:
			self.__dependency.evaluate(self.module.state)

	def _evaluate_rules(self):
		if self.rules is not None:
			self.rules.evaluate(self)