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

import abc

from arjuna.lib.unitee import Unitee
from arjuna.lib.unitee.enums import *
from arjuna.lib.unitee.reporter.result.types import *
from arjuna.lib.unitee.exceptions import *
import datetime

class TestObject(metaclass=abc.ABCMeta):
    def __init__(self, totype):
        self.__type = totype
        self.__tvars = None
        self.__thcount = 1
        self.__thname = None
        self.__iter = None
        self.__before_fixtures = []
        self.__after_fixtures = []
        self.__children = None
        self.__state = None
        self.__reported = False

    @property
    def reported(self):
        return self.__reported

    @reported.setter
    def reported(self, flag):
        self.__reported = flag

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def type(self):
        return self.__type

    @property
    def tvars(self):
        return self.__tvars

    @tvars.setter
    def tvars(self, tvars):
        self.__tvars = tvars

    @property
    def thcount(self):
        return self.__thcount

    @thcount.setter
    def thcount(self, count):
        self.__thcount = count

    @property
    def thname(self):
        return self.__thname

    @thname.setter
    def thname(self, name):
        self.__thname = name

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, cl):
        self.__children = cl
        self.__iter = iter(self.__children)

    def next(self):
        try:
            child = next(self.__iter)
            child.update_dynamic_tvars(self.tvars)
            return child
        except StopIteration:
            raise SubTestsFinished()

    def update_dynamic_tvars(self, tvars):
        self.tvars.evars.update(tvars.evars)

    @property
    def before_fixtures(self):
        return self.__before_fixtures

    def append_before_fixture(self, fix):
        if fix:
            self.__before_fixtures.append(fix)

    @property
    def after_fixtures(self):
        return self.__after_fixtures

    def append_after_fixture(self, fix):
        if fix:
            self.__after_fixtures.append(fix)

    def run(self, base_tvars=None):
        if base_tvars:
            self.tvars.evars.update(base_tvars.evars)
            self.tvars.dvars.update(base_tvars.dvars)

        try:
            self.evaluate_dependency()
        except DependencyNotMet as e:
            self.exclude(ResultCodeEnum.DEPENDENCY_NOT_MET, e.iid, ResultCodeEnum.PARENT_DEPENDENCY_NOT_MET)
            return

        bstamp = datetime.datetime.now().timestamp()
        if self.type not in {TestObjectTypeEnum.GSlot, TestObjectTypeEnum.MSlot}:
            info = Info(InfoType.STARTED, self)
            info.btstamp = bstamp
            Unitee.reporter.update_info(info)

        # Some test objects have multiple before fixtures e.f. init_each_group and init_group
        for before_fixture in self.before_fixtures:
            fresult = before_fixture.execute(self, self.tvars.clone())
            before_fixture.report()
            self.tvars.evars.update(before_fixture.tvars.evars)
            if fresult.has_issues():
                self.exclude(ResultCodeEnum["{}_{}".format(fresult.rtype, before_fixture.type.name)], fresult.iid)
                self.report_finish_info(bstamp)
                return
            # self.tvars.dvars.update(self.before_fixture.tvars.dvars)

        self._execute()

        if self.type != TestObjectTypeEnum.Test:
            if self.type not in {TestObjectTypeEnum.GSlot, TestObjectTypeEnum.MSlot}:
                for after_fixture in self.after_fixtures:
                    fresult = after_fixture.execute(self, self.tvars.clone())
                    if fresult.has_issues():
                        if self.type not in {TestObjectTypeEnum.GSlot, TestObjectTypeEnum.MSlot} and not self.reported:
                            result = TestObjectResult(
                                self, rtype=fresult.rtype,
                                rcode=ResultCodeEnum["{}_{}".format(fresult.rtype, after_fixture.type.name)],
                                iid=fresult.iid)
                            self.report(result)
                    else:
                        if self.type not in {TestObjectTypeEnum.GSlot, TestObjectTypeEnum.MSlot} and not self.reported:
                            result = TestObjectResult(self, rtype=ResultTypeEnum.PASS,
                                                      rcode=ResultCodeEnum.PASS_ALL_CHILD_TEST_OBJECTS)
                            self.report(result)
                    after_fixture.report()

                if not self.reported:
                    if self.state.has_failures():
                        result = TestObjectResult(self, rtype=ResultTypeEnum.FAIL,
                                                  rcode=ResultCodeEnum.FAIL_CHILD_TEST_OBJECT)
                        self.report(result)
                    elif self.state.has_errors():
                        result = TestObjectResult(self, rtype=ResultTypeEnum.ERROR,
                                                  rcode=ResultCodeEnum.ERROR_CHILD_TEST_OBJECT)
                        self.report(result)
                    elif self.state.has_exclusions():
                        result = TestObjectResult(self, rtype=ResultTypeEnum.EXCLUDED_CHILDREN,
                                                  rcode=ResultCodeEnum.EXCLUDED_CHILD_TEST_OBJECT)
                        self.report(result)
            # else:
            #     if self.type not in {TestObjectTypeEnum.GSlot, TestObjectTypeEnum.MSlot} and not self.reported:
            #         result = TestObjectResult(self, rtype=ResultTypeEnum.PASS,
            #                                   rcode=ResultCodeEnum.PASS_ALL_CHILD_TEST_OBJECTS)
            #         self.report(result)

        self.report_finish_info(bstamp)

    def report_finish_info(self, bstamp):
        if self.type not in {TestObjectTypeEnum.GSlot, TestObjectTypeEnum.MSlot}:
            info = Info(InfoType.FINISHED, self)
            info.btstamp = bstamp
            info.etstamp = datetime.datetime.now().timestamp()
            info.exec_time = info.etstamp - info.btstamp
            Unitee.reporter.update_info(info)

    @abc.abstractmethod
    def _execute(self):
        pass

    @abc.abstractmethod
    def _populate_tvars(self, base_tvars):
        pass

    @abc.abstractmethod
    def load(self, ptvars):
        pass

    def report(self, result):
        Unitee.reporter.update_result(result)
        self.reported = True

    def report_excluded(self, exclusion_type, issue_id):
        t = TestObjectResult(self, rtype=ResultTypeEnum.EXCLUDED, rcode=exclusion_type, iid=issue_id)
        self.report(t)

    def exclude(self, exclusion_type, issue_id, child_exclusion_type=None):
        if not child_exclusion_type:
            child_exclusion_type = exclusion_type
        if self.children:
            for child in self.children:
                child.exclude(child_exclusion_type, issue_id)
        self.report_excluded(exclusion_type, issue_id)

    def evaluate_dependency(self):
        pass