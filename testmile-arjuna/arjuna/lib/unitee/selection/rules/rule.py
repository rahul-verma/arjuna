
from arjuna.lib.unitee.validation import checks
from arjuna.lib.unitee.enums import *
from arjuna.lib.unitee.markup import mrules

from .enums import *
from .exceptions import *

def none(value):
    if type(value) is str:
        return value.lower() == "none" and None or value
    else:
        return value is None and None or value

converter_map = {
    'int': int,
    'str': str,
    'float': float,
    'bool': bool,
    'none' : none
}


value_checkers = {
    RuleConditionType.IS : checks.are_equal,
    RuleConditionType.MATCHES : checks.match_with_ignore_case,
    RuleConditionType.CONTAINS : checks.partially_match_with_ignore_case,
}

class Rule:
    def __init__(self, totype, is_inclusion_rule, target, robject, condition, expression, converter):
        self.totype = totype
        self.is_include_type = is_inclusion_rule
        self.target = target
        self.robject = robject
        self.condition = condition
        self.expression = expression
        self.converter = converter

    def __not_met_exc(self):
        raise RuleNotMet() #"Run time rules checking did not succeed for the test object.")

    def __raise_exception_for_check_result(self, check_result):
        if check_result:
            if self.is_include_type:
                return
            else:
                self.__not_met_exc()
        else:
            if self.is_include_type:
                self.__not_met_exc()
            else:
                return

    def evaluate(self, test_object):
        if test_object.type != self.totype:
            return

        include = False
        target_object_value = None
        if self.target == RuleTargetType.PROPS:
            o_container = None

            if test_object.type == TestObjectTypeEnum.Module:
                o_container = test_object.tvars.info.module
            elif test_object.type == TestObjectTypeEnum.Function:
                o_container = test_object.tvars.info.function
            else:
                return

            try:
                target_object_value = o_container.props[self.robject]
            except Exception as e:
                if self.is_include_type: self.__not_met_exc()
                return
            else:
                target_type = self.converter
                if not mrules.is_builtin_prop(self.robject):
                    target_type = type(target_object_value)
                succeeded = self.__call_checker(target_object_value, target_type)
                self.__raise_exception_for_check_result(succeeded)

        else:
            raise Exception("Not supported yet.")

    def __call_checker(self, target_object_value, target_type):
        actual = target_object_value
        expected = target_type(self.expression)
        if target_type is str:
            actual = actual and actual.lower() or None
            expected = expected and expected.lower() or None
        func = value_checkers[self.condition]
        return func(actual, expected)