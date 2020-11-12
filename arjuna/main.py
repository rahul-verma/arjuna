# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

import os # os is a operating system by  this module we can interact with our operating system , famous module provided by python  
import sys # it is a system module which can be used in various thing but some of them are sys.exit(1) is used to exit the condition 
import time # this time module is used to return time into seconds.

def main(*args):
    print("Executing Arjuna command line with args: {}".format(args))
    try:
        """
        by usnig try and exception we can print the errors occured during our programmes , as python is a interpreted language so it wil check line by line and if some error 
        occured it will stop to avoiding this we usually print that error in ecxception. when tries failed
        """"
        import signal
        import sys
        def signal_handler(sig, frame):
                print('Exiting...')
                sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        from arjuna import _ArjunFacade
        facade = _ArjunFacade()
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
