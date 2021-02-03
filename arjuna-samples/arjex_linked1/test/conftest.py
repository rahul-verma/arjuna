import pytest

from arjuna.engine.pytest import PytestHooks


def get_import_lenient_set(context):
    return set(["arjex_minimal.lib", "arjex_minimal.lib.resource", f"arjex_minimal.lib.resource." + context])

try:
    from arjex_minimal.lib.resource.group import *
except ModuleNotFoundError as e:
    if e.name not in get_import_lenient_set("group"):
        raise Exception(e.name)

try:
    from arjex_minimal.lib.resource.module import *
except ModuleNotFoundError as e:
    if e.name not in get_import_lenient_set("module"):
        raise Exception(e.name)

try:
    from arjex_minimal.lib.resource.test import *
except ModuleNotFoundError as e:
    if e.name not in get_import_lenient_set("test"):
        raise Exception(e.name)
