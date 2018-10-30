
from enum import Enum, auto

class RuleType(Enum):
    INCLUDE = auto()
    EXCLUDE = auto()

class RuleTargetType(Enum):
    PROPS = auto()
    EVARS = auto()

class RuleConditionType(Enum):
    IS = auto()
    MATCHES = auto()
    CONTAINS = auto()