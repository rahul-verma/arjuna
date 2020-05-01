import re
from enum import Enum, auto
from .ref import *

from arjuna.core.constant import *
from arjuna.core.error import *

class Pattern:

    @classmethod
    def extract(cls, pattern, target_str):
        return pattern.match(target_str)


class Rule:

    def __init__(self, rule_str, container, target, condition, expression):
        self.__rule_str = rule_str
        self.__container = container
        self.__target = target
        self.__condition = condition
        self.__expression = expression  
        self.__expression_type = type(expression)
        self.__checker = get_value_checker_for_symbol(self.__condition)

    @property
    def rule_str(self):
        return self.__rule_str

    @property
    def container(self):
        return self.__container

    @property
    def target(self):
        return self.__target

    @property
    def condition(self):
        return self.__condition

    @property
    def expression(self):
        return self.__expression    

    @property
    def expression_type(self):
        return self.__expression_type 

    @property
    def checker(self):
        return self.__checker 

    def _get_container_obj(self, obj):
        return getattr(obj, self.container)

    def __str__(self):
        return "{}(rule_str='{}', container={}, target={}, condition={}, expression={}, expression_type={}, checker={})".format(self.__class__.__name__, self.rule_str, self.container, self.target, self.condition, self.expression, self.expression_type.__name__, self.checker.__name__)

class BooleanPropPatternRule(Rule):
    '''
        Simple Pattern for Boolean built-in property or flags

        For example:

            unstable
            not unstable
    '''

    __NOT_PATTERN = re.compile(r"^\s*not\s+(?P<target>\w+)\s*$",re.IGNORECASE)
    __PATTERN = re.compile(r"^\s*(?P<target>\w+)\s*$",re.IGNORECASE)

    def __init__(self, *, rule_str, target, condition, expression):
        super().__init__(rule_str, "properties", target, condition, expression)

    @classmethod
    def _validate(cls, target):
        if is_builtin_prop(target) and get_value_type(target) is not bool:
            raise InvalidSelectionRule("Built-in property {} is not of bool type. It can not be used in a {} construct.".format(target, cls.__name__))

    @classmethod
    def from_str(cls, rule_str):  
        match = Pattern.extract(cls.__NOT_PATTERN, rule_str)
        if match:
            target = match.group('target')
            cls._validate(target)
            return BooleanPropPatternRule(**{
                'rule_str':rule_str, 
                'target': target,
                'condition' : RuleConditionType.NOT_EQUAL,
                'expression' : True
            })
        else:
            match = Pattern.extract(cls.__PATTERN, rule_str)
            if match:
                target = match.group('target')
                cls._validate(target)
                return BooleanPropPatternRule(**{
                'rule_str':rule_str, 
                'target': target,
                'condition' : RuleConditionType.EQUAL,
                'expression' : True
                })
            else:
                raise RulePatternDoesNotMatchError(rule_str, cls, "[not] <boolean_object>")

    def matches(self, obj):
        container = self._get_container_obj(obj)
        if not hasattr(container, self.target):
            actual = False
        else:
            actual = getattr(container, self.target)
        return self.checker(self.expression, actual)


class TagsPatternRule(Rule):
    '''
        Simple Pattern for presence/absence of tag(s).

        For example:

            with tags a,b
            without tags a,b
            with bugs a,b
            without bugs a,b
            with envs a,b
            without envs a,b

            You can use singular version as well - **tag/bug/env**
    '''

    __WITH_PATTERN = re.compile(r"^\s*with\s+(?P<container>(.+?))\s+(?P<tags>(.*))$",re.IGNORECASE)
    __WITHALL_PATTERN = re.compile(r"^\s*withall\s+(?P<container>(.+?))\s+(?P<tags>(.*))$",re.IGNORECASE)
    __WITHOUT_PATTERN = re.compile(r"^\s*without\s+(?P<container>(.+?))\s+(?P<tags>(.*))$",re.IGNORECASE)

    def __init__(self, *, rule_str, container, target, condition, expression):
        super().__init__(rule_str, container, target, condition, expression)

    @property
    def tags(self):
        return self.__tags

    @classmethod
    def __convert_to_tags(cls, expression):
        return set([p.strip().lower() for p in expression.split(",")])

    @classmethod
    def from_str(cls, rule_str):  
        condition = None
        match = Pattern.extract(cls.__WITH_PATTERN, rule_str)
        if match:
            condition = RuleConditionType.HAS_INTERSECTION
        else:
            match = Pattern.extract(cls.__WITHALL_PATTERN, rule_str)
            if match:
                condition = RuleConditionType.IS_SUBSET
            else:
                match = Pattern.extract(cls.__WITHOUT_PATTERN, rule_str)
                if match:
                    condition = RuleConditionType.NO_INTERSECTION
                else:
                    raise RulePatternDoesNotMatchError(rule_str, cls, "[with|withall|without]  <tag-container> tag1[,....]")

        tags = cls.__convert_to_tags(match.group('tags'))
        container = get_tag_container(match.group('container'))
        return TagsPatternRule(**{
            'rule_str':rule_str,
            'container' : container,
            'target': tags, 
            'condition' : condition,
            'expression': tags
        })        

    def matches(self, obj):
        container = self._get_container_obj(obj)
        if container is None:
            container = set()
        if not container and self.condition == RuleConditionType.IS_SUBSET:
            return False
        return self.checker(self.expression, container)

class PropertyPatternRule(Rule):
    '''
        Pattern for executing a condition on a property value.

        For example:

            author is Rahul
    '''
    condition_str = "is|not|eq|=|==|!=|ne|lt|<|le|<=|gt|>|ge|>=|matches|~=|contains|\*="
    p5_raw = r"^\s*(?P<target>\w+)\s+(?P<condition>({}){{1,1}})\s+(?P<expression>.*?)\s*$".format(condition_str)

    __PATTERN = re.compile(p5_raw, re.IGNORECASE)

    def __init__(self, *, rule_str, target, condition, expression):
        super().__init__(rule_str, "properties", target, condition, expression)

    @classmethod
    def from_str(cls, rule_str):  
        match = Pattern.extract(cls.__PATTERN, rule_str)
        if match:
            target = match.group('target')
            target_type = get_value_type(target) 
            return PropertyPatternRule  (**{
                'rule_str':rule_str,                 
                'target': target, 
                'condition' : convert_to_condition(target, target_type, match.group('condition')), 
                'expression': convert_expression(target, target_type, match.group('expression')),
            })
        else:
            raise RulePatternDoesNotMatchError(rule_str, cls, "<prop_name> <condition> <expression>")

    def matches(self, obj):
        container = self._get_container_obj(obj)
        if not hasattr(container, self.target):
            actual = get_default_value_for_type(self.expression_type, self.target)
        else:
            actual = getattr(container, self.target)

        return self.checker(actual, self.expression)


class Selector:

    def __init__(self):
        self.__rules = list()

    def add_rule(self, rule_str):
        self.__rules.append(self.__build_rule(rule_str))

    def __build_rule(self, rule_str):
        pattern = None
        try:
            return BooleanPropPatternRule.from_str(rule_str)
        except RulePatternDoesNotMatchError:
            try:
                return TagsPatternRule.from_str(rule_str)
            except RulePatternDoesNotMatchError:
                try:
                    return PropertyPatternRule.from_str(rule_str)
                except RulePatternDoesNotMatchError:
                    raise Exception("Rule is invalid: " + rule_str)

    @property
    def rules(self):
        return self.__rules

    def __str__(self):
        return str([str(r) for r in self.__rules])
