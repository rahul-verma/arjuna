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

import inspect
from decimal import ROUND_HALF_EVEN

from arjuna.lib.enums import *
from .testpoint import *
from arjuna.unitee.enums import *
from arjuna.unitee.reporter.result.types import *
from .assertion import *

class _Asserter:

    def __init__(self, purpose):
        self.__purpose = purpose

    @property
    def purpose(self):
        return self.__purpose

    def evaluate(self):
        pass

    def _is_soft_asserter(self):
        return False

    def assert_that(self, subject):
        assertion = LinkedAssertion(self, subject)
        return assertion

class _SoftAsserter(_Asserter):

    def __init__(self, purpose):
        super().__init__(purpose)
        self.__steps = []

    def _add_step(self, step):
        self.__steps.append(step)

    def _is_soft_asserter(self):
        return True

    def evaluate(self):
        for step in self.__steps:
            step.evaluate()

class _LazyAsserter(_SoftAsserter):

    def __init__(self, purpose):
        super().__init__(purpose)
        self.__assertions = []

    def execute(self):
        for assertion in self.__assertions:
            assertion.execute()

    def _add_assertion(self, assertion):
        self.__assertions.append(assertion)

    def assert_that(self, subject):
        assertion = PendingAssertion(self, subject)
        return assertion

class Steps:

    @staticmethod
    def __step(src, step_type, step_result_type, purpose, expectation, observation, assert_message, **kwargs):
        step = Step()
        step.step_type = step_type
        step.purpose = purpose
        step.relation = "-"
        step.step_props = kwargs
        step.source = src

        if expectation is not None and observation is not None:
            step.expectation = expectation
            step.observation = observation
        elif expectation is None and observation is None:
            pass
        else:
            raise Exception("Expectation and Actual observation should be provided or ignored together.")

        if step_result_type == ResultTypeEnum.NOTHING:
            step.rtype = "-"
        elif step_result_type == ResultTypeEnum.FAIL:
            step.set_failure()
        elif step_result_type == ResultTypeEnum.ERROR:
            step.set_error()

        step.assert_message = assert_message and assert_message or "-"

        step.add_to_state()
        step.evaluate()

    # Plan to include take_screenshot=False as a keyword argument for different steps.
    # Also plan to have a screenshot step.
    # Also plan to capture the exception trace in the step and issue info.

    @staticmethod
    def passed(purpose, *, expectation=None, observation=None,  **kwargs):
        src = Steps.__get_caller()
        Steps.__step(src, StepType.ExecStep, ResultTypeEnum.PASS, purpose, expectation, observation, None, **kwargs)

    @staticmethod
    def failed(purpose, *, expectation=None, observation=None, message=None, **kwargs):
        src = Steps.__get_caller()
        Steps.__step(src, StepType.ExecStep, ResultTypeEnum.FAIL, purpose, expectation, observation, message, **kwargs)

    @staticmethod
    def erred(purpose, message=None, **kwargs):
        src = Steps.__get_caller()
        Steps.__step(src, StepType.ExecStep, ResultTypeEnum.ERROR, purpose, None, None, message, **kwargs)

    @staticmethod
    def log(purpose, **kwargs):
        from arjuna.tpi import Arjuna
        logger = Arjuna.get_logger()
        logger.debug(purpose)
        src = Steps.__get_caller()
        Steps.__step(src, StepType.LogStep, ResultTypeEnum.NOTHING, purpose, None, None, None, **kwargs)

    @staticmethod
    def __get_caller():
        frame = inspect.stack()[2]
        return "{}.py:{}:L{}".format(inspect.getmodule(frame[0]).__name__, frame[3], frame[2])

    @staticmethod
    def validate(purpose):
        return _Asserter(purpose)

    @staticmethod
    def soft_validate(purpose):
        return _SoftAsserter(purpose)

    @staticmethod
    def lazy_validate(purpose):
        return _LazyAsserter(purpose)

    @staticmethod
    def assert_true(purpose, actual):
        assertion = Assertion(purpose, actual)
        assertion.is_true()

    @staticmethod
    def assert_false(purpose, actual):
        assertion = Assertion(purpose, actual)
        assertion.is_false()

    @staticmethod
    def assert_equal(purpose, actual, expected):
        assertion = Assertion(purpose, actual)
        assertion.is_equal_to(expected)

    @staticmethod
    def assert_not_equal(purpose, actual, expected):
        assertion = Assertion(purpose, actual)
        assertion.is_not_equal_to(expected)

    @staticmethod
    def assert_almost_equal(purpose, actual, expected, max_offset=None, rounded_as=ROUND_HALF_EVEN):
        assertion = Assertion(purpose, actual)
        assertion.with_max_offset(max_offset)
        assertion.rounded_as(rounded_as)
        assertion.is_equal_to(expected)

    @staticmethod
    def assert_same(purpose, actual, expected):
        assertion = Assertion(purpose, actual)
        assertion.is_same_as(expected)

    @staticmethod
    def assert_not_same(purpose, actual, expected):
        assertion = Assertion(purpose, actual)
        assertion.is_not_same_as(expected)

    assert_different = assert_not_same

    @staticmethod
    def assert_none(purpose, actual):
        assertion = Assertion(purpose, actual)
        assertion.is_none()

    @staticmethod
    def assert_not_none(purpose, actual):
        assertion = Assertion(purpose, actual)
        assertion.is_not_none()

    @staticmethod
    def assert_includes(purpose, container, content):
        assertion = Assertion(purpose, container)
        assertion.includes(content)

    @staticmethod
    def assert_excludes(purpose, container, content):
        assertion = Assertion(purpose, container)
        assertion.excludes(content)