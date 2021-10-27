import pytest

from arjuna.engine.pytest import PytestHooks


try:
    from arjex_seamful_demo.lib.hook.resource import *
except ModuleNotFoundError as e:
    if e.name not in {"arjex_seamful_demo.lib", "arjex_seamful_demo.lib.hook", "arjex_seamful_demo.lib.hook.resource"}:
        raise

