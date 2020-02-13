from importlib import import_module

mod = import_module("arjex_webui_basics.lib.fixtures")

names = ["get_number"]

for name in names:
    globals()[name] = getattr(mod, name)

__all__ = names