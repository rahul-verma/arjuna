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

import datetime

from collections import OrderedDict

from arjuna.lib.adv.types import CIStringDict
from arjuna.unitee.enums import *
from arjuna.lib.utils import thread_utils

class DictWrapper:

    def __init__(self, header_enum, sdict=None):
        vars(self)['_d'] = OrderedDict()
        for henum in header_enum:
            self.__update(henum.name.lower(), "-", False)
        if sdict:
            self.update_from_dict(sdict)

    def __getattr__(self, item):
        if item.startswith("_"): return vars(self)[item]
        else:
            self.__validate_attr(item)
            return self._d[item.lower()]

    def __setattr__(self, attr, value):
        if attr.startswith("_"):
            vars(self)[attr] = value
            return
        self.__update(attr, value)

    def headers(self):
        return tuple(self._d.keys())

    def values(self):
        return tuple(self._d.values())

    def get_dict(self):
        return self._d

    def items(self):
        return self._d.items()

    def __validate_attr(self, k):
        if k.lower() not in self._d:
            raise AttributeError("{} is not an allowed result attribute for {}".format(k, self.__class__.__name__))

    def __update(self, k, v, validate=True):
        if validate:
            self.__validate_attr(k)
        self._d[k.lower()] = v

    def update_from_dict(self, d):
        for i,j in d.items():
            self.__update(i,j)

class ReportEntry(DictWrapper):
    def __init__(self, entry_enum, obj):
        super().__init__(entry_enum)
        self.otype = obj.type.name
        self.session = obj.tvars.info.session.meta["name"]
        if obj.tvars.info.stage:
            self.stage = obj.tvars.info.stage.meta["name"]
        if obj.tvars.info.group:
            self.group = obj.tvars.info.group.meta["name"]
        if obj.tvars.info.module:
            self.pkg = obj.tvars.info.module.meta["pkg"]
            self.module = obj.tvars.info.module.meta["name"]
        if obj.tvars.info.function:
            self.function = obj.tvars.info.function.meta["name"]
        if obj.tvars.info.test_num:
            self.test = obj.tvars.info.test_num

class Result(ReportEntry):

    def __init__(self, obj):
        super().__init__(ResultEntryEnum, obj)

    def is_stepped(self):
        return False

class StepResult(DictWrapper):
    def __init__(self):
        super().__init__(StepEntryEnum)

class IssueEntry(DictWrapper):
    def __init__(self):
        super().__init__(IssueEntryEnum)

class Info(ReportEntry):

    def __init__(self, info_type, obj):
        super().__init__(InfoEntryEnum, obj)
        self.info_timestamp = datetime.datetime.now().timestamp()
        self.message = info_type.name.lower()

class FixtureInfo(Info):
    def __init__(self, fix, info_type, obj):
        super().__init__(info_type, obj)
        self.otype = TestObjectTypeEnum.FIXTURE
        self.fixture = fix.fqname
        self.fixtype = fix.ftype

class TestObjectResult(Result):

    def __init__(self, test_obj, *, rtype=None, rcode=None, iid=None):
        super().__init__(test_obj)
        self.result_timestamp = datetime.datetime.now().timestamp()
        self.rtype = rtype and rtype.name or "-"
        self.rcode = rcode and rcode.name or "-"
        self.iid = iid and iid or "-"
        self._issues = []
        self._steps = []
        if not test_obj.tvars.evars.is_empty():
            self.evars = str(test_obj.tvars.evars)
        if not test_obj.tvars.tags.is_empty():
            self.tags = str(test_obj.tvars.tags)
        if test_obj.type == TestObjectTypeEnum.Module:
            if not test_obj.tvars.info.module.props.is_empty():
                self.props = test_obj.tvars.info.module.props
        elif test_obj.type in {TestObjectTypeEnum.Function, TestObjectTypeEnum.Test}:
            if not test_obj.tvars.info.module.props.is_empty() and not test_obj.tvars.info.function.props.is_empty():
                parts = []
                parts.append("Module Props")
                parts.append(str(test_obj.tvars.info.module.props))
                parts.append("Function Props")
                parts.append(str(test_obj.tvars.info.function.props))
                self.props = "\n".join(parts)
        if not test_obj.tvars.runtime.is_empty():
            self.runtime = str(test_obj.tvars.runtime)
        self.thread_id = thread_utils.get_current_thread_name()

    @property
    def steps(self):
        return self._steps

    def is_stepped(self):
        return False

    @property
    def issues(self):
        return self._issues

    def has_issues(self):
        return len(self._issues) !=0

    def append_issue(self, issue):
        issue_entry = IssueEntry()
        issue_entry.update_from_dict(self)
        issue_entry.issue_timestamp = issue.issue_timestamp
        issue_entry.result_timestamp = "-"
        issue_entry.rtype = "-"
        issue_entry.rcode = "-"
        issue_entry.iid = str(issue.iid)
        issue_entry.itype = issue.itype.name
        issue_entry.ename = issue.ename
        issue_entry.emsg = issue.emsg
        issue_entry.etrace = issue.etrace
        if self.iid == "-":
            self.iid = issue.iid
        self._issues.append(issue_entry)

    def append_step_issue(self, sr, issue):
        issue_entry = IssueEntry()
        issue_entry.update_from_dict(self)
        issue_entry.update_from_dict(sr)
        issue_entry.issue_timestamp = issue.issue_timestamp
        issue_entry.result_timestamp = "-"
        issue_entry.rtype = "-"
        issue_entry.rcode = "-"
        issue_entry.iid = str(issue.iid)
        issue_entry.itype = issue.itype.name
        issue_entry.ename = issue.ename
        issue_entry.emessage = issue.emsg
        issue_entry.etrace = issue.etrace
        if self.iid == "-":
            self.iid = issue.iid
        self._issues.append(issue_entry)

    def get_reportable(self):
        class Reportable:
            def __init__(this):
                this.result = OrderedDict()
                this.result.update(self.items())
                this.steps = self._steps
            def has_steps(this):
                return len(this.steps) > 0

        return Reportable()

SessionResult = TestObjectResult
StageResult = TestObjectResult
GroupResult = TestObjectResult
ModuleResult = TestObjectResult
FunctionResult = TestObjectResult

class SteppedResult(TestObjectResult):

    def __init__(self, test_obj):
        super().__init__(test_obj)

    def is_stepped(self):
        return True

    def get_step_type(self):
        pass

    def __create_step_result(self, step):
        sr = StepResult()
        sr.otype = step.otype
        sr.step_rtype = step.rtype == "-" and step.rtype or step.rtype.name
        sr.iid = step.iid
        sr.step_timestamp = step.timestamp
        sr.step_exec_context = step.exec_context.name
        sr.step_type = step.step_type.name
        sr.step_id = step.step_num
        sr.step_source = step.source
        sr.purpose = step.purpose
        sr.observation = step.observation
        sr.expectation = step.expectation
        sr.assert_message = step.assert_message
        sr.step_props = str(step.step_props)
        if step.has_issue():
            self.append_step_issue(sr, step.issue)
        self._steps.append(sr)

    def set_steps(self, step_list):
        for step in step_list:
            if self.rtype != ResultTypeEnum.FAIL.name:
                if step.failed():
                    self.rtype = ResultTypeEnum.FAIL.name
                    self.rcode = "{}_STEP_FAILURE".format(self.otype.upper())
                    self.iid = step.iid
                elif step.erred():
                    self.rtype = ResultTypeEnum.ERROR.name
                    self.rcode = "{}_STEP_ERROR".format(self.otype.upper())
                    self.iid = step.iid
            self.__create_step_result(step)

class FixtureResult(SteppedResult):

    def __init__(self, test_obj, fixture):
        super().__init__(test_obj)
        self.otype = TestObjectTypeEnum.Fixture.name
        self.fixture = fixture.qname
        self.fixtype = fixture.type.name
        self.evars = str(fixture.tvars.evars)
        self.data_record = "-"

    def set_steps(self, step_list):
        if not step_list:
            self.rtype = "PASS"
            self.rcode = "NO_STEPS_RECORDED"
            return

        super().set_steps(step_list)

class TestResult(SteppedResult):

    def __init__(self, test_obj):
        super().__init__(test_obj)
        self.otype = TestObjectTypeEnum.Test.name
        if not test_obj.tvars.data.record.is_empty():
            self.data_record = test_obj.tvars.data.record

    def set_steps(self, step_list):
        if not step_list:
            self.rtype = "NOT_A_TEST"
            self.rcode = "NO_STEPS_RECORDED"
            return

        super().set_steps(step_list)

# class Issue(DictWrapper):
#
#     def __init__(self, test_obj, *, iid, itype, istype, ename, emessage, trace):
#         super().__init__(IssueEntryEnum)
#         base = Info("-", test_obj)
#         self.update_from_dict(base.items())
#         self.issue_timestamp = datetime.datetime.now().timestamp()
#         self.iid = iid
#         self.itype = itype.name
#         self.istype = istype.name
#         self.ename = ename
#         self.emessage = emessage
#         self.trace = trace