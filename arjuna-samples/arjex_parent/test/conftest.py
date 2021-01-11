import pytest

from arjuna.engine.pytest import PytestHooks


try:
    from arjex_linked1.lib.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex_linked1.lib", "arjex_linked1.lib.resource"}:
        raise Exception(e.name)

try:
    from arjex_linked2.lib.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex_linked2.lib", "arjex_linked2.lib.resource"}:
        raise Exception(e.name)

try:
    from arjex_parent.lib.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex_parent.lib", "arjex_parent.lib.resource"}:
        raise Exception(e.name)

