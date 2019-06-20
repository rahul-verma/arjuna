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

import re
import inspect
from decimal import getcontext, Decimal, ROUND_HALF_EVEN

from arjuna.unitee.validation import checks
from .testpoint import *
import math
import re

class Assertion:
    def __init__(self, purpose, subject):
        self.__purpose = purpose
        self.__subject = subject
        self.__offset = "0.00000000000000000001"
        self.__rounding = ROUND_HALF_EVEN
        self._step = None

    def __create_step(self):
        self._step = Step()
        self._step.purpose = self.__purpose
        frame = inspect.stack()[3]
        self._step.source = "{}.py:{}:L{}".format(inspect.getmodule(frame[0]).__name__, frame[3], frame[2])
        self._step.step_type = StepType.AssertStep

    def evaluate(self):
        self._step.evaluate()

    def _configure_step(self):
        self._step.add_to_state()
        self._step.evaluate()

    def is_true(self):
        self.__create_step()
        self._step.expectation = "Should be True"
        try:
            if checks.is_true(self.__subject):
                self._step.observation = "True"
                self._step.assert_message = "Assertion fulfilled."
            else:
                self._step.observation = "False"
                self._step.set_failure()
                self._step.assert_message = "Condition is False."
        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)
        self._configure_step()

    def is_false(self):
        self.__create_step()
        self._step.expectation = "Should be False"
        try:
            if checks.is_true(self.__subject):
                self._step.observation = "True"
                self._step.set_failure()
                self._step.assert_message = "Condition is True."
            else:
                self._step.observation = "False"
                self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def __update_check_for_null_expected_object(step):
        step.set_error()
        step.assert_message = "Expected object can not be None"
        step.observation = "Error: An error occured before this could be evaluated."

    def __set_check_error_for_assertion_issue(self, e):
        self._step.set_error()
        self._step.assert_message = "Error in assertion. {}".format(e)

    def is_equal_to(self, expected):
        if type(self.__subject) is float or type(expected) is float:
            return self.__is_almost_equal_to(expected)
        self.__create_step()
        has_failed = False
        try:
            if checks.is_none(expected):
                if checks.is_none(self.__subject):
                    pass  # None = None
                else:
                    has_failed = True

            type_mismatch = False
            matched = False
            if type(self.__subject) is not type(self.__subject):
                if type(self.__subject) in {'int', 'float'} and type(expected) in {'int', 'float'}:
                    pass
                else:
                    type_mismatch = True
                    has_failed = True
                    # we need to handle this
            if not type_mismatch:
                self._step.expectation = 'Should be equal to Object of type={0} and value=>{1}<'.format(type(expected).__name__, expected)
                self._step.observation = 'Object of type={0} and value=>{1}<'.format(type(self.__subject).__name__, self.__subject)

                has_failed = checks.are_not_equal(self.__subject, expected)

                if has_failed:
                    self._step.set_failure()
                    self._step.assert_message = "Objects are not equal"
                else:
                    self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def is_not_equal_to(self, expected):
        self.__create_step()
        has_failed = False
        try:
            if checks.is_none(expected):
                if checks.is_none(self.__subject):
                    has_failed = False
                else:
                    pass

            type_mismatch = False
            matched = False
            if type(self.__subject) is not type(self.__subject):
                if type(self.__subject) in {'int', 'float'} and type(expected) in {'int', 'float'}:
                    pass
                else:
                    type_mismatch = True
                    has_failed = True
                    # we need to handle this

            if not type_mismatch:
                self._step.expectation = 'Should not be equal to Object of type={0} and value=>{1}<'.format(type(expected).__name__, expected)
                self._step.observation = 'Object of type={0} and value=>{1}<'.format(type(self.__subject).__name__, self.__subject)

                has_failed = checks.are_equal(self.__subject, expected)

                if has_failed:
                    self._step.set_failure()
                    self._step.assert_message = "Objects are equal"
                else:
                    self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def rounded_as(self, strategy):
        self.__rounding = strategy
        return self

    def with_max_offset(self, offset):
        if offset is None:
            return
        if type(offset) in {int, float}:
            f_offset = Decimal(offset).quantize(Decimal("0.0001"))
            if f_offset <= 0 or f_offset >= 1:
                raise Exception("Max offset provided as float should be a non-negative value such that 0 < offset < 1 after rounding to 4 decimal places.")
            self.__offset = re.sub(r"[0]+$", "", str(f_offset))
        elif type(offset) is str:
            try:
                f_offset = float(offset)
                if f_offset <= 0 or f_offset >= 1:
                    raise Exception(
                        "Max offset provided as string should be a non-negative value such that 0 < offset < 1.")
                else:
                    self.__offset = offset
            except:
                raise Exception("Max offset string must contain a floating number.")
        else:
            raise Exception("Max offset can be a float or string")
        return self

    def __is_almost_equal_to(self, expected):
        self.__create_step()
        has_failed = False
        try:

            not_allowed = False
            lhs = self.__subject
            rhs = expected
            allowed_type_set = {int, float}
            if type(expected) in allowed_type_set and type(self.__subject) in allowed_type_set:
                zero, places = self.__offset.split('.', 1)
                precision = len(places)
                allowed_diff = Decimal(self.__offset)
                try:
                    lhs = Decimal(lhs).quantize(allowed_diff, rounding=self.__rounding)
                except Exception as e:
                    print(e)
                    import traceback
                    traceback.print_exc()
                    # No rounding or offsetting needed as decimal places are less than offset precision
                    lhs = Decimal(lhs)
                try:
                    rhs = Decimal(rhs).quantize(allowed_diff, rounding=self.__rounding)
                except Exception as f:
                    print(f)
                    rhs = Decimal(rhs)

                diff = abs(lhs-rhs)
                has_failed = diff > allowed_diff
            else:
                not_allowed = True

            self._step.expectation = 'Should be equal to approxmiately >{}<.{}{}'.format(
                expected,
                ' Max Offset specified: {}.'.format(allowed_diff),
                " Round as per offset with {} strategy.".format(self.__rounding)
            )

            self._step.observation = '>{}<'.format(self.__subject)

            if not_allowed:
                self._step.set_failure()
                self._step.assert_message = ">{0}<[type:{1}] can not be approxmiately compared to >{2}<[type:{3}]".format(
                    self.__subject,
                    type(self.__subject).__name__,
                    expected,
                    type(expected).__name__
                )
            elif has_failed:
                self._step.set_failure()
                self._step.assert_message = "Numbers are not equal as per approximation guidelines."
            else:
                self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def is_same_as(self, expected):
        self.__create_step()
        has_failed = False
        try:
            if checks.is_none(expected):
                if checks.is_none(self.__subject):
                    pass
                else:
                    has_failed = True

            else:
                self._step.expectation = "Should be same as Object of type >{0}< and id >{1}<".format(type(expected).__name__, id(expected))
                self._step.observation = "Object of type >{0}< and id >{1}<".format(type(self.__subject).__name__, id(self.__subject))

                has_failed = checks.are_not_same(self.__subject, expected)

                if has_failed:
                    self._step.set_failure()
                    self._step.assert_message = "Objects are not same."
                else:
                    self._step.assert_message = "Assertion fulfilled."


        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()


    def is_not_same_as(self, expected):
        self.__create_step()
        has_failed = False
        try:
            if checks.is_none(expected):
                if checks.is_none(self.__subject):
                    has_failed = True
                else:
                    pass
            else:
                self._step.expectation = "Should not be same as Object of type >{0}< and id >{1}<".format(type(expected).__name__, id(expected))
                self._step.observation = "Object of type >{0}< and id >{1}<".format(type(self.__subject).__name__,
                                                                                  id(self.__subject))

                has_failed = checks.are_same(self.__subject, expected)

                if has_failed:
                    self._step.set_failure()
                    self._step.assert_message = "Objects are same."
                else:
                    self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    is_different_from = is_not_same_as


    def is_none(self):
        self.__create_step()
        self._step.expectation = "Should be None"
        try:
            if checks.is_not_none(self.__subject):
                self._step.set_failure()
                self._step.observation = "Object of type {0} with id = {1}".format(type(self.__subject).__name__, id(self.__subject))
                self._step.assert_message = "Object is not None"
            else:
                self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()


    def is_not_none(self):
        self.__create_step()
        self._step.expectation = "Should NOT be None"
        try:
            if checks.is_none(self.__subject):
                self._step.set_failure()
                self._step.observation = "None"
                self._step.assert_message = "Supplied object is None."
            else:
                self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def includes(self, content):
        self.__create_step()
        self._step.expectation = "Any iterable containing {}".format(content)
        try:
            has_failed = False
            if checks.is_none(self.__subject):
                has_failed = True
                self._step.observation = "None"
                self._step.assert_message = "Container is None."
            elif type(self.__subject) not in {list, tuple, set, dict}:
                has_failed = True
                self._step.assert_message = "Container is not of type list, tuple, set or dict."
            else:
                self._step.observation = "Object of type={0} and contents=<{1}>".format(type(self.__subject).__name__,
                                                                                        str(self.__subject))
                if type(content) in {list, tuple, set}:
                    for item in content:
                        if item not in self.__subject:
                            has_failed = True
                            self._step.assert_message = "One or more items not included in object."
                            break
                elif type(content) is dict:
                    if type(self.__subject) is dict:
                        for k,v in content.items():
                            if k not in self.__subject or self.__subject[k] != v:
                                has_failed = True
                                self._step.assert_message = "One or more items not included in object."
                                break
                    else:
                        has_failed = True
                        self._step.assert_message = "Container is not of type dict. Attempt to find dict in non-dict failed."
                else:
                    if content not in self.__subject:
                        has_failed = True
                        self._step.assert_message = "Content not included in object."
            if has_failed:
                self._step.set_failure()
            else:
                self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def excludes(self, content):
        self.__create_step()
        self._step.expectation = "Any iterable NOT containing {}".format(content)
        try:
            has_failed = False
            if checks.is_none(self.__subject):
                has_failed = True
                self._step.observation = "None"
                self._step.assert_message = "Container is None."
            elif type(self.__subject) not in {list, tuple, set, dict}:
                has_failed = True
                self._step.assert_message = "Container is not of type list, tuple, set or dict."
            else:
                self._step.observation = "Object of type={0} and contents=<{1}>".format(type(self.__subject).__name__,
                                                                                        str(self.__subject))
                if type(content) in {list, tuple, set}:
                    for item in content:
                        if item in self.__subject:
                            has_failed = True
                            self._step.assert_message = "One or more items included in object."
                            break
                elif type(content) is dict:
                    if type(self.__subject) is dict:
                        for k,v in content.items():
                            if k in self.__subject and self.__subject[k] == v:
                                has_failed = True
                                self._step.assert_message = "One or more items included in object."
                                break
                    else:
                        has_failed = True
                        self._step.assert_message = "Container is not of type dict. Attempt to find dict in non-dict failed."
                else:
                    if content in self.__subject:
                        has_failed = True
                        self._step.assert_message = "Content included in object."
            if has_failed:
                self._step.set_failure()
            else:
                self._step.assert_message = "Assertion fulfilled."

        except Exception as e:
            self.__set_check_error_for_assertion_issue(e)

        self._configure_step()

    def execute(self):
        pass

class LinkedAssertion(Assertion):
    def __init__(self, stepper, subject):
        super().__init__(stepper.purpose, subject)
        self._stepper = stepper

    def _configure_step(self):
        if not self._stepper._is_soft_asserter():
            super()._configure_step()
        else:
            self._step.add_to_state()
            self._stepper._add_step(self._step)


class PendingAssertion(Assertion):
    def __init__(self, stepper, subject):
        super().__init__(stepper.purpose, subject)
        self._stepper = stepper
        self.__pending_func = None
        self.__pending_args = None

    def __assign_caller(self, func, args):
        self.__pending_func = func
        self.__pending_args = args
        self._stepper._add_assertion(self)

    def is_true(self, *vargs):
        self.__assign_caller(super().is_true, vargs)

    def is_false(self, *vargs):
        self.__assign_caller(super().is_false, vargs)

    def is_equal_to(self, *vargs):
        self.__assign_caller(super().is_equal_to, vargs)

    def is_not_equal_to(self, *vargs):
        self.__assign_caller(super().is_not_equal_to, vargs)

    def is_same_as(self, *vargs):
        self.__assign_caller(super().is_same_as, vargs)

    def is_not_same_as(self, *vargs):
        self.__assign_caller(super().is_not_same_as, vargs)

    is_different_from = is_not_same_as

    def is_none(self, *vargs):
        self.__assign_caller(super().is_none, vargs)

    def is_not_none(self, *vargs):
        self.__assign_caller(super().is_not_none, vargs)

    def includes(self, *vargs):
        self.__assign_caller(super().includes, vargs)

    def excludes(self, *vargs):
        self.__assign_caller(super().excludes, vargs)

    def execute(self):
        if self.__pending_args:
            self.__pending_func(*self.__pending_args)
        else:
            self.__pending_func()

    def _configure_step(self):
        if not self._stepper._is_soft_asserter():
            super()._configure_step()
        else:
            self._step.add_to_state()
            self._stepper._add_step(self._step)