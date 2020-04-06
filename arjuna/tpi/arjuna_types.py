from typing import TypeVar
from arjuna.tpi.enums import ArjunaOption

ListOrTuple = TypeVar('ListOrTuple', list, tuple)
ArjunaOptionOrStr = TypeVar('ArjunaOptionOrStr', ArjunaOption, str)