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

from arjuna.unitee.types.root import Root
from arjuna.unitee.enums import *

from arjuna.unitee.reporter.result.types import FixtureResult
from arjuna.unitee.enums import ResultCodeEnum
from arjuna.unitee.exceptions import *

class Fixture(Root):
    def __init__(self, fixdef):
        super().__init__()
        self.name = fixdef.name
        self.qname = fixdef.qname
        self.type = fixdef.type
        self.func = fixdef.func
        self.__tvars = None
        self._result = None

    @property
    def tvars(self):
        return self.__tvars

    def __process_tvars_from_tobj(self, tvars):
        self.__tvars = tvars
        self.tvars.function['name'] = self.name
        self.tvars.function['qname'] = self.qname
        self.tvars.object['type'] = "FIXTURE"
        self.tvars.object['name'] = "Fixture"

    def execute(self, test_obj, tvars):
        from arjuna.unitee import Unitee
        self.__tvars = tvars
        result = None
        issue = False
        steps = None
        utvars = None
        try:
            self.unitee.state_mgr.get_current_thread_state().begin_recording(ExecutionContext.Fixture)
            utvars = self.__tvars.create_utvars()
            self.func(utvars)
        except StepResultEvent as sre:
            pass
            # We would assume the step exception added by Step itself
        except Exception as e:
            self.unitee.state_mgr.get_current_thread_state().add_step_exception(e, traceback.format_exc())

        self.tvars.context.update_from_context(utvars.context)
        steps = self.unitee.state_mgr.get_current_thread_state().end_recording()
        fresult = FixtureResult(test_obj, self)
        fresult.set_steps(steps)
        self._result = fresult
        return fresult

    def report(self):
        from arjuna.unitee import Unitee
        self.unitee.reporter.update_result(self._result)