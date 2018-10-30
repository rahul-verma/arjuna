
from arjuna.lib.unitee.markup import mrules
from arjuna.lib.unitee.enums import *

from .enums import *
from .rule import *

symbols_map = {
    '=' : 'is',
    '==' : 'is',
    '~=' : 'matches',
    '*=' : 'contains'
}

class RuleBuilder:

    def __init__(self):
        self.__totype = None
        self.__is_include_type = RuleType.INCLUDE
        self.__target = None
        self.__robject = None
        self.__condition = None
        self.__expression = None
        self.__converter = None


    def test_object_type(self, totype):
        self.__totype = TestObjectTypeEnum[totype]
        return self

    def rule_type(self, rtype):
        self.__is_include_type = RuleType[rtype.upper().strip()] == RuleType.INCLUDE
        return self

    def rule_object(self, target_name):
        self.__robject = target_name.lower()
        if target_name.upper() in BuiltInProp.__members__:
            self.__target = RuleTargetType.PROPS
            self.__converter = mrules.get_value_type(target_name)
            print(self.__converter)
        return self

    def condition(self, condition):
        try:
            if condition in symbols_map:
                condition = symbols_map[condition]
            self.__condition = RuleConditionType[condition.upper()]
        except:
            raise Exception("Invalid condition supplied in rule: " + condition)
        return self

    def expression(self, expression):
        self.__expression = expression
        return self

    def build(self):
        if not self.__totype:
            raise Exception("Test object not defined for rule.")
        elif not self.__target:
            raise Exception("Target container not defined for rule.")
        elif not self.__robject:
            raise Exception("Target object not defined for rule.")
        elif not self.__condition:
            raise Exception("Condition not defined for rule.")
        elif not self.__expression:
            raise Exception("Expression not defined for rule.")

        return Rule(
            self.__totype,
            self.__is_include_type,
            self.__target,
            self.__robject,
            self.__condition,
            self.__expression,
            self.__converter
        )