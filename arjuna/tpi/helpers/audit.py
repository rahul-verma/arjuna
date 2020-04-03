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

import time
import inspect

class Stack:

    @classmethod
    def get_invoker(cls):
        frame = inspect.stack()[2]
        mod = inspect.getmodule(frame[0])
        mod_name = mod.__name__
        mod_file = mod.__file__
        mod_script = ""
        if mod_name == "__main__":
            mod_script = "Script:<{}> at ".format(mod_file)
        else:
            mod_script = "Module:<{}> File:<{}>".format(mod_name, mod_file)
        func = frame[3]
        if func == "<module>":
            func = ""
        else:
            func = "Function/Method: <{}> in ".format(func)
        line = frame[2]
        return "{}{}Line: {}".format(func, mod_script, line)

class HardCoded:

    @classmethod
    def __log(cls, invoker, why, seconds):
        from arjuna import Arjuna
        Arjuna.get_logger().warning("Hardcoded sleep executed for {} seconds by {}. Reason by author: {}".format(seconds, invoker, why))

    @classmethod
    def sleep(cls, why, seconds):
        time.sleep(seconds)
        cls.__log(Stack.get_invoker(), why, seconds)