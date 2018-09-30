import os
import sys
import time

def join_paths(*paths):
    return os.path.abspath(os.path.join(*paths))

root_dir = join_paths(os.path.realpath(__file__), "..")
tm_arjuna_dir = join_paths(root_dir, "testmile-arjuna")
importables_dir = join_paths(tm_arjuna_dir, "third_party", "py_importables")

sys.path.insert(0, tm_arjuna_dir)
sys.path.insert(0, importables_dir)
sys.path.insert(0, root_dir)

try:
    from arjuna.lib import Arjuna
    Arjuna.launch(sys.argv)
except Exception as e:
    # The following sleep is to accommodate a common IDE issue of
    # interspersing main exception with console output.
    time.sleep(0.5)
    msg = '''
{0}
Sorry. Looks like this is an error Arjuna couldn't handle.
If Arjuna should handle this error, write to us: support@testmile.com
{0}

Message: {1}
    '''.format("-" * 70, str(e))
    print(msg)
    import traceback
    print(traceback.format_exc())
