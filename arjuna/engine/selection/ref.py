# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna.core import checks
from arjuna.core.constant import BuiltInProp, RuleConditionType, RuleTargetType
from arjuna.core.error import InvalidSelectionRule

def none(value):
    if type(value) is str:
        return value.lower() == "none" and None or value
    else:
        return value is None and None or value

def custom_bool(value):
    if type(value) is bool:
        return value
    elif value.lower() in BOOL_MAP:
        return BOOL_MAP[value.lower()]
    else:
        raise InvalidSelectionRule(f"Provided unexpected value >>{value}<< for boolean context in rule. Allowed: [true/false/on/off/yes/no/0/1]")

built_in_prop_type = {
    BuiltInProp.PACKAGE : str,
    BuiltInProp.MODULE : str,
    BuiltInProp.NAME : str,
    BuiltInProp.QUAL_NAME : str,
    BuiltInProp.ID : str,
    BuiltInProp.PRIORITY : int,
    BuiltInProp.NAME : str,
    BuiltInProp.AUTHOR : str,
    BuiltInProp.IDEA : str,
    BuiltInProp.UNSTABLE : bool,
    BuiltInProp.COMPONENT : str,
    BuiltInProp.APP_VERSION : str,
    BuiltInProp.LEVEL : str,
    BuiltInProp.REVIEWED : bool,
}

BOOL_MAP = {
    'true': True,
    'false': False,
    'on': True,
    'off': False,
    'yes' : True,
    'no' : False
}

SYMBOLS_MAP = {
    'is': 'equal',
    'not': 'not_equal',
    'eq': 'equal',
    '=': 'equal',
    '==': 'equal',
    '!=': 'not_equal',
    'ne': 'not_equal',
    '~=': 'matches',
    '!~=': 'does_not_match',
    'matches': 'matches',
    '*=': 'partially_matches',
    '!*=': 'does_not_partially_match',
    'lt': 'less_than',
    '<': 'less_than',
    'le': 'less_or_equal',
    '<=': 'less_or_equal',
    'gt': 'greater_than',
    '>': 'greater_than',
    'ge': 'greater_or_equal',
    '>=': 'greater_or_equal',
}

def get_all_symbols():
    return SYMBOLS_MAP.keys()

__str_symbols = {
    'matches',
    '~=',
    '!~=',
    '\!~=',
    '*=',
    '!*=',
    '\!*=',
    'is',
    'not',
    'eq',
    'ne',
    '!=',
    '=',
    '==',
}

__number_symbols =  {
    'is',
    'not',
    'eq',
    'ne',
    '=',
    '==',
    '!=',
    'lt',
    '<',
    'le',
    '<=',
    'gt',
    '>',
    'ge',
    '>='
}

__appver_symbols = __str_symbols.union(__number_symbols)
__str_symbols = __str_symbols.union(__number_symbols)

__priority_symbols =  {
    'is' : 'is',
    'not': 'not',
    'eq': 'eq',
    'ne': 'ne',
    '=': '=',
    '==': '==',
    '!=': '!=',
    'lt': 'gt',
    '<': '>',
    'le': 'ge',
    '<=': '>=',
    'gt': 'lt',
    '>': '<',
    'ge': 'le',
    '>=': '<=',
}

# __str_rules = {
#     RuleConditionType.EQUAL, 
#     RuleConditionType.MATCHES, 
#     RuleConditionType.CONTAINS, 
#     RuleConditionType.PARTIALLY_MATCHES
# }

# __number_rules =  {
#     RuleConditionType.EQUAL,
#     RuleConditionType.NOT_EQUAL,
#     RuleConditionType.LESS_THAN,
#     RuleConditionType.LESS_OR_EQUAL,
#     RuleConditionType.GREATER_THAN,
#     RuleConditionType.GREATER_OR_EQUAL
# }

# __appver_rules = __str_rules.union(__number_rules)

# ALLOWED_CONDITIONS = {
#     str : __str_rules,
#     bool : {
#             RuleConditionType.EQUAL, 
#             RuleConditionType.NOT_EQUAL
#         },
#     int : __number_rules,
#     float : __number_rules
# }

ALLOWED_SYMBOLS = {
    str: __str_symbols,
    bool: ['is', 'not', '=', '==', 'eq', '!=', 'ne'],
    int: __number_symbols,
    float: __number_symbols
}

VALUE_CHECKERS = {
    RuleConditionType.EQUAL : checks.are_equal,
    RuleConditionType.NOT_EQUAL : checks.are_not_equal,
    RuleConditionType.LESS_THAN : checks.less_than,
    RuleConditionType.LESS_OR_EQUAL : checks.less_or_equal,
    RuleConditionType.GREATER_THAN : checks.greater_than,
    RuleConditionType.GREATER_OR_EQUAL : checks.greater_or_equal,
    RuleConditionType.MATCHES : checks.match_with_ignore_case,
    RuleConditionType.DOES_NOT_MATCH : checks.does_not_match_with_ignore_case,
    RuleConditionType.PARTIALLY_MATCHES : checks.partially_match_with_ignore_case,
    RuleConditionType.DOES_NOT_PARTIALLY_MATCH : checks.does_not_partially_match_with_ignore_case,
    RuleConditionType.CONTAINS : checks.contains,
    RuleConditionType.IS_SUBSET : checks.is_subset,
    RuleConditionType.HAS_INTERSECTION : checks.has_intersection,
    RuleConditionType.NO_INTERSECTION : checks.has_no_intersection,
}

CONVERTER_MAP = {
    int: int,
    str: str,
    float : float,
    bool: custom_bool
}

def _validate_symbol(symbol):
    if symbol not in SYMBOLS_MAP:
        raise InvalidSelectionRule("Invalid condition symbol >>{}<< used. Allowed: {}".format(symbol, tuple(SYMBOLS_MAP.keys())))

def _validate_allowed_symbol(target, target_type, symbol):
    if target == "app_version":
        if symbol not in __appver_symbols:
            raise InvalidSelectionRule("For app_version property, you have used an unexpected condition [{}]. Allowed: {}.".format(symbol, __appver_symbols))
    elif symbol not in ALLOWED_SYMBOLS[target_type]:
        raise InvalidSelectionRule("[{}] property is of type [{}]. You have used an unexpected condition [{}]. Allowed: {}.".format(target, target_type.__name__, symbol, ALLOWED_SYMBOLS[target_type]))

def convert_to_condition(target, target_type, symbol):
    symbol = symbol.strip().lower()
    _validate_symbol(symbol)
    _validate_allowed_symbol(target, target_type, symbol)
    if target != "priority":
        return RuleConditionType[SYMBOLS_MAP[symbol].upper()]
    else:
        return RuleConditionType[SYMBOLS_MAP[__priority_symbols[symbol]].upper()]


def get_value_checker_for_symbol(condition):
    return VALUE_CHECKERS[condition]

def convert_expression(target, target_type, expression):
    if expression.lower().strip() == 'none':
        return None
    if is_builtin_prop(target):
        return CONVERTER_MAP[target_type](expression)
    else:
        return expression

ALLOWED_TAG_CONTAINERS = {'tag', 'tags', 'bug', 'bugs', 'env', 'envs'}

TAG_CONTAINER_MAP = {
    'tag': 'tags', 
    'tags': 'tags', 
    'bug': 'bugs',  
    'bugs': 'bugs', 
    'env': 'envs', 
    'envs': 'envs' 
}

def get_tag_container(container):
    container = container.strip().lower()
    if container in ALLOWED_TAG_CONTAINERS:
        #raise InvalidSelectionRule("Unrecognized tag container [{}]. Allowed: {}".format(container, ALLOWED_TAG_CONTAINERS))
        return TAG_CONTAINER_MAP[container]
    else:
        return container

def validate_built_in_props(props):
    for k,v in props.items():
        if is_builtin_prop(k.upper()):
            expected_type = built_in_prop_type[BuiltInProp[k.upper()]]
            actual_type = type(v)
            if v is not None and actual_type is not expected_type:
                raise Exception("Built-in property {} should of type {}. Found {} of type {}".format(
                    k,
                    expected_type,
                    v,
                    actual_type
                ))

def get_value_type(built_in_prop_name):
    return built_in_prop_type[BuiltInProp[built_in_prop_name.upper()]]

def is_builtin_prop(name):
    return name.upper() in BuiltInProp.__members__

__type_defaults = {
    bool: False,
    str: None,
    int: None,
    float: None
}
def get_default_value_for_type(in_type, name):
    if name == "priority":
        return 5
    elif name == "app_version":
        return "0.0.0"
    else:
        return __type_defaults[in_type]
