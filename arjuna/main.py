import os
import sys
import time

def main(args=None):
    try:
        import signal
        import sys
        def signal_handler(sig, frame):
                print('Exiting...')
                sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        from arjuna import Arjuna
        Arjuna.launch(args and args or sys.argv)
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
