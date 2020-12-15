import pytest

from arjuna.engine.pytest import PytestHooks


try:
    from arjex_pytest.lib.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex_pytest.lib", "arjex_pytest.lib.resource"}:
        raise Exception(e.name)

