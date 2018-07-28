import sys
import time
sys.path.insert(0,'.')
sys.path.insert(0,'./third_party/py_importables')

try:
    from arjuna.lib import Arjuna
    Arjuna.launch(sys.argv)
except Exception as e:
    # The following sleep is to accomodate IDEs issue of interspersing main exception with console output.
    time.sleep(0.5)
    msg = '''
{0}
Sorry. Looks like this is an error Arjuna couldn't handle.
If Arjuna should handle this error, write to us: support@testmile.com
{0}

Message: {1}
    '''.format("-" * 70, str(e))
    print (msg)
    import traceback
    print (traceback.format_exc())
