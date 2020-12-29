import pytest

from arjuna.engine.pytest import PytestHooks


try:
    from arjex.lib.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex.lib", "arjex.lib.resource"}:
        raise Exception(e.name)

