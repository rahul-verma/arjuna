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

import traceback

from .base import TestObject
from arjuna.unitee import Unitee
from arjuna.unitee.reporter.result.types import *
from arjuna.unitee.enums import *
from arjuna.unitee.exceptions import *


class Test(TestObject):

	def __init__(self, num, group, module, func):
		super().__init__(TestObjectTypeEnum.Test)
		self.num = num
		self.group = group
		self.module = module
		self.func = func
		self.func_obj = func.func_obj
		self.append_before_fixture(self.module.fixture_defs.build(FixtureTypeEnum.INIT_EACH_TEST))
		self.append_after_fixture(self.module.fixture_defs.build(FixtureTypeEnum.END_EACH_TEST))

	def load(self, base_tvars):
		self._populate_tvars(base_tvars)

	def _populate_tvars(self, base_tvars):
		self.tvars = base_tvars
		self.tvars.info.test_num = self.num
		self.tvars.info.object_type = TestObjectTypeEnum.Test.name
		# print("while setting", self.num, self.tvars.data.record)

	def _execute(self):

		self.unitee.state_mgr.get_current_thread_state().begin_recording(ExecutionContext.Test)
		try:
			utvars = self.tvars.create_utvars()
			# print(self.func_obj)
			self.func_obj(utvars)
			# print("source", self.num, self.tvars.data.record)
			# print("dest", self.num, utvars.data.record)
		except StepResultEvent as e:
			pass
			# Step addition would have happended as a result of step.evaluate()
		except Exception as e:
			self.unitee.state_mgr.get_current_thread_state().add_step_exception(e, traceback.format_exc())

		steps = self.unitee.state_mgr.get_current_thread_state().end_recording()
		tresult = TestResult(self)
		tresult.set_steps(steps)

		test_reported = False
		if tresult.has_issues():
			test_reported = True
			self.report(tresult)

		for after_fixture in self.after_fixtures:
			fresult = after_fixture.execute(self, self.tvars.clone())
			if fresult.has_issues():
				after_fixture.report()
				if not test_reported:
					tresult.rtype = fresult.rtype
					tresult.rcode = ResultCodeEnum["{}_{}".format(fresult.rtype, after_fixture.type.name)].name
					tresult.iid = fresult.iid
					self.report(tresult)
					test_reported = True
			else:
				if not test_reported:
					if tresult.rtype == "-":
						tresult.rtype = ResultTypeEnum.PASS.name
						tresult.rcode = ResultCodeEnum.PASS_ALL_STEPS.name
					self.report(tresult)
					test_reported = True
					after_fixture.report()

		if not test_reported:
			if tresult.rtype == "-":
				tresult.rtype = ResultTypeEnum.PASS.name
				tresult.rcode = ResultCodeEnum.PASS_ALL_STEPS.name
			self.report(tresult)

	def report(self, result):
		super().report(result)
		self.func.state.update(result)
		self.func.state.test_summary.increment(ResultTypeEnum[result.rtype])