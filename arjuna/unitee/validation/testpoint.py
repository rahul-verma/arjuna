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

from arjuna.lib.exceptions import *
from arjuna.lib.types import constants
from arjuna.lib.utils import thread_utils
from arjuna.unitee.exceptions import *
from arjuna.unitee.enums import *
from arjuna.unitee.types.containers import CIStringDict
import datetime

class Issue:
    def __init__(self, *, iid, itype, ename, emsg, etrace):
        self.issue_timestamp = datetime.datetime.now().timestamp()
        self.iid = iid
        self.itype = itype
        self.ename = ename
        self.emsg = emsg
        self.etrace = etrace

class __BaseTestPoint:
    def __init__(self):
        self.__otype = None
        self.__tstamp = datetime.datetime.now().timestamp()
        self.__counter = "-"
        self.__exec_context = ExecutionContext.Test
        self.__step_type = StepType.ExecStep
        self.__purpose = constants.NOTSET_STRING
        self.__expectation = constants.NOTSET_STRING
        self.__observation = constants.NOTSET_STRING
        self.__assert_message = constants.NOTSET_STRING
        self.__has_failed = False
        self.__has_erred = False
        self.__iid = "-"
        self.__rtype = ResultTypeEnum.PASS
        self.__issue = None
        self.__step_props = "-"
        self.__source = "-"

        from arjuna.tpi import Arjuna
        self.unitee = Arjuna.get_unitee_instance()

    @property
    def otype(self):
        return self.__otype

    @otype.setter
    def otype(self, o_type):
        self.__otype = o_type

    @property
    def step_props(self):
        return self.__step_props

    @step_props.setter
    def step_props(self, props):
        self.__step_props = props and CIStringDict(props) or "-"

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        self.__source = source and source or "-"

    @property
    def timestamp(self):
        return self.__tstamp

    @property
    def exec_context(self):
        return self.__exec_context

    @exec_context.setter
    def exec_context(self, exec_context):
        self.__exec_context = exec_context


    @property
    def step_type(self):
        return self.__step_type

    @step_type.setter
    def step_type(self, step_type):
        self.__step_type = step_type

    @property
    def issue(self):
        return self.__issue

    @issue.setter
    def issue(self, issue):
        self.__issue = issue

    def has_issue(self):
        return self.__issue is not None

    @property
    def iid(self):
        return self.__iid

    @iid.setter
    def iid(self, iid):
        self.__iid = iid

    @property
    def rtype(self):
        return self.__rtype

    @rtype.setter
    def rtype(self, rtype):
        self.__rtype = rtype

    @property
    def step_num(self):
        return self.__counter

    @step_num.setter
    def step_num(self, num):
        self.__counter = num

    @property
    def purpose(self):
        return self.__purpose

    @purpose.setter
    def purpose(self, purpose):
        if purpose is not None:
            self.__purpose = purpose

    def __trim_str(self, val):
        if val is not None and len(val) > 25000:
            return messages.Common.STR_LIMIT
        else:
            return val

    @property
    def expectation(self):
        return self.__expectation

    @expectation.setter
    def expectation(self, expectation):
        self.__expectation = self.__trim_str(expectation)

    @property
    def observation(self):
        return self.__observation

    @observation.setter
    def observation(self, observation):
        self.__observation = self.__trim_str(observation)

    @property
    def assert_message(self):
        return self.__assert_message

    @assert_message.setter
    def assert_message(self, message):
        self.__assert_message = self.__trim_str(message)

    def passed(self):
        return ((not self.failed() and not self.erred()))

    def failed(self):
        return self.__has_failed

    def set_failure(self):
        self.__has_failed = True
        self.rtype = ResultTypeEnum.FAIL

    def erred(self):
        return self.__has_erred

    def set_error(self):
        self.__has_erred = True
        self.rtype = ResultTypeEnum.ERROR

    def add_to_state(self):
        if self.failed():
            self.unitee.state_mgr.get_current_thread_state().add_fstep(self)
        elif self.erred():
            self.unitee.state_mgr.get_current_thread_state().add_estep(self)
        else:
            self.unitee.state_mgr.get_current_thread_state().add_pstep(self)


    def evaluate(self):
        if self.failed() or self.erred():
            raise StepResultEvent(self)

class Step(__BaseTestPoint):
    def __init__(self, ptname=None):
        super().__init__()
        self.ptname = ptname and ptname or thread_utils.get_current_thread_name()
