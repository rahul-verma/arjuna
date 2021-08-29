import pytest

from arjuna.engine.pytest import PytestHooks


try:
    from arjex.lib.hook.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex.lib", "arjex.lib.hook", "arjex.lib.hook.resource"}:
        raise

