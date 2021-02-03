# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import time

def main(*args, ext_engine=False):
    print("Executing Arjuna command line with args: {}".format(args))
    try:
        import signal
        import sys
        def signal_handler(sig, frame):
                print('Exiting...')
                sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        from arjuna import _ArjunFacade
        facade = _ArjunFacade()
        # For external test engine, Arjuna is loaded but it does not itself execute tests.
        if ext_engine:
            facade.load(args and args or sys.argv)
        else:
            facade.launch(args and args or sys.argv)
    except Exception as e:
        # The following sleep is to accommodate a common IDE issue of
        # interspersing main exception with console output.
        time.sleep(0.5)
        msg = '''
    {0}
    Sorry. Looks like this is an error Arjuna couldn't handle.
    Create a bug report on GitHub: https://github.com/rahul-verma/arjuna
    {0}

    Message: {1}
        '''.format("-" * 70, str(e))
        print(msg)
        import traceback
        print(traceback.format_exc())
