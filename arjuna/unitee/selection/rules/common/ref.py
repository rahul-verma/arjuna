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

from .enums import *
from .utils import *
from arjuna.unitee.validation import checks

BOOL_MAP = {
    'true': True,
    'false': False,
    'on': True,
    'off': False,
    '1': True,
    '0': False,
    'yes' : True,
    'no' : False
}

SYMBOLS_MAP = {
    'eq': 'is',
    '=': 'is',
    '==': 'is',
    '~=': 'matches',
    '*=': 'partially_matches',
    'lt': 'less_than',
    'le': 'less_or_equal',
    'gt': 'greater_than',
    'ge': 'greater_or_equal',
}

__number_rules =  {
    RuleConditionType.IS,
    RuleConditionType.LESS_THAN,
    RuleConditionType.LESS_OR_EQUAL,
    RuleConditionType.GREATER_THAN,
    RuleConditionType.GREATER_OR_EQUAL
}

__number_symbols =  [
    'is',
    'eq',
    '=',
    '==',
    'lt',
    'le',
    'gt',
    'ge'
]

ALLOWED_CONDITIONS = {
    str : {RuleConditionType.IS, RuleConditionType.MATCHES, RuleConditionType.CONTAINS, RuleConditionType.PARTIALLY_MATCHES},
    bool : {RuleConditionType.IS},
    int : __number_rules,
    float : __number_rules
}

ALLOWED_SYMBOLS = {
    str: ['is', 'eq', '=', '==', 'matches', 'contains'],
    bool: ['is'],
    int: __number_symbols,
    float: __number_symbols
}

VALUE_CHECKERS = {
    RuleConditionType.IS : checks.are_equal,
    RuleConditionType.LESS_THAN : checks.less_than,
    RuleConditionType.LESS_OR_EQUAL : checks.less_or_equal,
    RuleConditionType.GREATER_THAN : checks.greater_than,
    RuleConditionType.GREATER_OR_EQUAL : checks.greater_or_equal,
    RuleConditionType.MATCHES : checks.match_with_ignore_case,
    RuleConditionType.PARTIALLY_MATCHES : checks.partially_match_with_ignore_case,
    RuleConditionType.CONTAINS : checks.contains,
}


PROPERTY_CONTAINER_MAP = {
    'prop': RuleTargetType.PROPS,
    'evar': RuleTargetType.EVARS,
    'tag': RuleTargetType.TAGS,
    'bug': RuleTargetType.BUGS,
}

CONTAINER_MAP = {
    'props': RuleTargetType.PROPS,
    'evars': RuleTargetType.EVARS,
    'tags': RuleTargetType.TAGS,
    'bugs': RuleTargetType.BUGS,
}

CONVERTER_MAP = {
    'int': int,
    'str': str,
    'float': float,
    'bool': custom_bool,
    'none' : none
}