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
from arjuna.lib.thread.decorators import *
from arjuna.unitee.reporter.result import *
from arjuna.unitee.exceptions import *
from arjuna.lib.exceptions import *
from arjuna.lib.utils import thread_utils
from arjuna.unitee.enums import *
from arjuna.unitee.validation.testpoint import *

import traceback

from arjuna.unitee.enums import *

class _SummaryResult:
    def __init__(self):
        self.summary = {i: 0 for i in ResultTypeEnum}

    def increment(self, type):
        self.summary[type] += 1

    def succeeded(self):
        return self.summary[ResultTypeEnum.PASS] > 0 \
               and self.summary[ResultTypeEnum.FAIL] == 0 \
               and self.summary.get[ResultTypeEnum.ERROR] == 0\
                and self.summary.get[ResultTypeEnum.EXCLUDED] == 0

    def has_issues(self):
        return not self.succeeded()

    def has_failures(self):
        return self.summary[ResultTypeEnum.FAIL] > 0

    def has_errors(self):
        return self.summary[ResultTypeEnum.ERROR] > 0

    def has_exclusions(self):
        return self.summary[ResultTypeEnum.EXCLUDED] > 0 or self.summary[ResultTypeEnum.EXCLUDED_CHILDREN] > 0

    def update_from_summary_result(self, summary):
        for k,v in summary.summary.items():
            self.summary[k] = self.summary[k] + v

class _ThreadState:

    def __init__(self):
        self.lock = threading.RLock()
        self.logger = Arjuna.get_logger()
        self.__current_steps = None
        self.__current_context = None
        self.unitee = Arjuna.get_unitee_instance()

    def get_steps(self):
        return tuple(self.__current_steps)

    def begin_recording(self, context):
        self.__current_steps = []
        self.__current_context = context

    def end_recording(self):
        self.__current_context = None
        return self.__current_steps

    @sync_method('lock')
    def __add_step(self, step):
        step.exec_context = self.__current_context
        if self.__current_context == ExecutionContext.Test:
            step.otype = "TestStep"
        else:
            step.otype = "FixtureStep"
        self.__current_steps.append(step)

    @sync_method('lock')
    def __get_step_id(self):
        return len(self.__current_steps) + 1

    @sync_method('lock')
    def add_pstep(self, step):
        step.step_num = self.__get_step_id()
        self.__add_step(step)

    @sync_method('lock')
    def add_fstep(self, step):
        step.step_num = self.__get_step_id()
        issue = self.__create_issue_for_problem_step(ResultTypeEnum.FAIL)
        step.issue = issue
        step.iid = issue.iid
        self.__add_step(step)

    @sync_method('lock')
    def add_estep(self, step):
        step.step_num = self.__get_step_id()
        issue = self.__create_issue_for_problem_step(ResultTypeEnum.ERROR)
        step.issue = issue
        step.iid = issue.iid
        self.__add_step(step)

    @sync_method('lock')
    def add_step_exception(self, e, strace):
        step = self.__create_step_result_for_exception(self.__get_step_id(), e, strace)
        self.__add_step(step)

    def __create_step_result_for_exception(self, step_num, e, strace):
        try:
            if isinstance(e, Failure):
                return self.__create_step_failure(step_num, e, strace)
            elif isinstance(e, AssertionError):
                return self.__create_py_step_failure(step_num, e, strace)
            elif isinstance(e, Error):
                return self.__create_step_error(step_num, e, strace)
            elif isinstance(e, Problem):
                return self.__create_py_step_error(step_num, e, strace)
            else:
                return self.__create_py_step_error(step_num, e, strace)
        except Exception as f:
            return self.__create_py_step_error(step_num, f, traceback.format_exc())

    def __create_issue(self, e, strace, i_type):
        return self.unitee.state_mgr.create_issue_from_exception(e, strace, i_type)

    def __create_issue_for_problem_step(self, i_type):
        return self.unitee.state_mgr.create_issue_for_problem_step(i_type)

    def __create_step_failure(self, step_num, e, strace):
        issue = self.__create_issue(e, strace, ResultTypeEnum.FAIL)
        step = e.step
        step.rtype = issue.itype
        step.step_num = step_num
        step.issue = issue
        step.iid = issue.iid
        return step

    def __create_py_step_failure(self, step_num, e, strace):
        issue = self.__create_issue(e, strace, ResultTypeEnum.FAIL)
        step = Step()
        step.iid = issue.iid
        step.rtype = ResultTypeEnum.FAIL
        step.step_num = step_num
        step.issue = issue
        step.set_failure()
        return step

    def __create_step_error(self, step_num, e, strace):
        issue = self.__create_issue(e, strace, ResultTypeEnum.ERROR)
        step = e.step
        step.rtype = issue.itype
        step.step_num = step_num
        step.issue = issue
        step.iid = issue.iid
        return step

    def __create_py_step_error(self, step_num, e, strace):
        issue = self.__create_issue(e, strace, ResultTypeEnum.ERROR)
        step = Step()
        step.iid = issue.iid
        step.rtype = ResultTypeEnum.ERROR
        step.step_num = step_num
        step.issue = issue
        step.set_error()
        return step

class SummaryState:
    def __init__(self):
        self.logger = Arjuna.get_logger()
        self.summary_result = _SummaryResult()
        self.test_summary = _SummaryResult()

    def increment(self, rtype):
        self.summary_result.increment(rtype)

    def update(self, result):
        rtype =  ResultTypeEnum[result.rtype]
        self.increment(rtype)

    def update_test_summary_from_state(self, state):
        self.test_summary.update_from_summary_result(state.test_summary)

    def has_issues(self):
        return self.summary_result.has_issues()

    def has_failures(self):
        return self.summary_result.has_failures()

    def has_errors(self):
        return self.summary_result.has_errors()

    def has_exclusions(self):
        return self.summary_result.has_exclusions()

class StateWithIssueMgt(SummaryState):

    def __init__(self):
        super().__init__()
        self.__issues_map = {}

    def update(self, result):
        rtype =  ResultTypeEnum[result.rtype]
        self.increment(rtype)
        name = self._get_child_name(result)
        iid = result.iid

        if rtype in {ResultTypeEnum.FAIL, ResultTypeEnum.ERROR, ResultTypeEnum.EXCLUDED}:
            self.__issues_map[name] = iid

    def _get_child_name(self, result):
        pass

    def raise_on_problem(self, name):
        if name in self.__issues_map:
            raise DependencyNotMet(self.__issues_map[name])

SessionState = SummaryState
StageState = SummaryState
FunctionState = SummaryState

class GroupState(StateWithIssueMgt):
    def __init__(self):
        super().__init__()

    def _get_child_name(self, result):
        return ".".join([result.pkg, result.module])

class ModuleState(StateWithIssueMgt):
    def __init__(self):
        super().__init__()

    def _get_child_name(self, result):
        return result.function

class ThreadManager:
    def __init__(self):
        self.lock = threading.RLock()
        self.logger = Arjuna.get_logger()

        self.__thread_states = {}
        self.__current_issue_counter = 0

    @sync_method('lock')
    def get_current_thread_state(self):
        return self.__thread_states.get(thread_utils.get_current_thread_name())

    @sync_method('lock')
    def get_thread_state(self, tname):
        return self.__thread_states.get(tname)

    @sync_method('lock')
    def register_thread(self, name):
        self.__thread_states[name] = _ThreadState()

    @sync_method('lock')
    def deregister_thread(self, t_name):
        del self.__thread_states[t_name]

    def __get_issue_id(self):
        self.__current_issue_counter += 1
        return self.__current_issue_counter

    @sync_method('lock')
    def create_issue_from_exception(self, e, strace, i_type):
        issue_id = self.__get_issue_id()
        issue = Issue(
            iid = issue_id,
            itype = i_type,
            ename = e.__class__.__name__,
            emsg = str(e),
            etrace = strace
        )

        return issue

    @sync_method('lock')
    def create_issue_for_problem_step(self, i_type):
        issue_id = self.__get_issue_id()
        issue = Issue(
            iid = issue_id,
            itype = i_type,
            ename = "StepException",
            emsg = "Step {}. Refer Step info.".format(i_type.name.lower()),
            etrace = "-"
        )

        return issue