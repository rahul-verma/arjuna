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

import inspect
import os
import re
import sys
from urllib3.util import parse_url
from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.core.types.constants import *

class Validator:
    VNREGEX = r'^([a-zA-Z][a-zA-Z_0-9]{2,50})$'
    VNREGEX_TEXT = '''
    Name must be a string of length 3-50 starting with a letter, followed by letters, digits or _ (underscore).
    '''

    @classmethod
    def raise_exc(cls, input, msg=None):
        curframe = inspect.currentframe()
        callframe = inspect.getouterframes(curframe, 2)
        caller = callframe[1][3]
        msg = msg is not None and msg + "." or ""
        raise Exception("{} is not {}. {}".format(input, caller, msg))

    @classmethod
    def str(cls, input):
        if type(input) not in {str, int, float, bool}:
            cls.raise_exc(input)
        return str(input)

    @classmethod
    def bool(cls, input):
        if type(input) is not bool:
            if type(input) is str:
                if input.lower() in TRUES:
                    return True
                elif input.lower() in FALSES:
                    return False
                else:
                    cls.raise_exc(input)
            else:
                cls.raise_exc(input)
        return input

    @classmethod
    def int(cls, input):
        if type(input) is not int:
            if type(input) is str:
                try:
                    return int(input)
                except:
                    cls.raise_exc(input)
            else:
                cls.raise_exc(input)
        return input

    @classmethod
    def float(cls, input):
        if type(input) is not float:
            if type(input) is int:
                return float(input)
            elif type(input) is str:
                try:
                    return float(input)
                except:
                    cls.raise_exc(input)
            else:
                cls.raise_exc(input)
        return input

    @classmethod
    def absolute_dir_path_present(cls, input):
        if type(input) is not str:
            cls.raise_exc(input)
        elif not os.path.isabs(input) or not os.path.isdir(input):
            cls.raise_exc(input)
        return input

    @classmethod
    def absolute_dir_path(cls, input):
        if type(input) is not str:
            cls.raise_exc(input)
        elif os.path.exists(input):
            if not os.path.isabs(input) or not os.path.isdir(input):
                cls.raise_exc(input)
        # else:
        #     os.makedirs(input)
        return input

    @classmethod
    def absolute_file_path(cls, input):
        if type(input) is not str:
            cls.raise_exc(input)
        elif not os.path.isabs(input) or not os.path.isfile(input):
            cls.raise_exc(input)
        return input

    @classmethod
    def guiauto_automator_name(cls, input):
        try:
            return GuiAutomatorName[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def guiauto_context_name(cls, input):
        try:
            return GuiAutomationContext[input.upper()]
        except Exception as e:
            print(e)
            cls.raise_exc(input)

    @classmethod
    def logging_level(cls, input):
        try:
            return LoggingLevel[input.upper()]
        except Exception as e:
            print(e)
            cls.raise_exc(input)

    @classmethod
    def locale(cls, input):
        try:
            return Locale[input.upper()]
        except Exception as e:
            print(e)
            cls.raise_exc(input)

    @classmethod
    def str_list(cls, input):
        if type(input) is not list:
            cls.raise_exc(input)
        else:
            if not input:
                return input
            s = {type(i) for i in input}
            if s != {type("")}:
                cls.raise_exc(input)
        return input

    @classmethod
    def allowed_log_contexts(cls, input):
        if type(input) is str:
            input = [i.strip().lower() for i in input.split(",")]
            input = set(input)
        elif type(input) in {set, list, tuple}:
            input = set([i.lower() for i in input])
        else:
            cls.raise_exc(input)    

        input.add("default")
        return input 

    @classmethod
    def str_or_strlist(cls, input):
        if type(input) is str:
            input = [i.strip().lower() for  i in input.split(",")]
        elif type(input) in {set, list, tuple}:
            input = [i.lower() for i in input if i not in input]
        else:
            cls.raise_exc(input)
        return list(dict.fromkeys(input)) 

    @classmethod
    def actor_mode(cls, input):
        try:
            return SetuActorMode[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def browser_name(cls, input):
        try:
            if isinstance(input, BrowserName):
                return input
            return BrowserName[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def desktop_os(cls, input):
        try:
            return DesktopOS[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def report_formats(cls, input):
        l = None
        try:
            if type(input) is str:
                return cls.report_formats([i.upper() for i in input.split(",")])
            elif type(input) in {list, tuple}:
                return [ReportFormat[i.upper()] for i in input]
        except:
            cls.raise_exc(input)

    @classmethod
    def mobile_os(cls, input):
        try:
            return MobileOsName[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def positive_int(cls, input):
        if type(input) is int and input <= 1:
            cls.raise_exc(input)
        if type(input) is not int:
            i = cls.int(input)
            if i <= 1:
                cls.raise_exc(input)
            else:
                return i
        return input

    @classmethod
    def positive_float(cls, input):
        if type(input) is float and input < 0.1:
            cls.raise_exc(input)

        if type(input) is not float:
            i = cls.float(input)
            if i <= 1:
                cls.raise_exc(input)
            else:
                return i
        return input

    @classmethod
    def web_url(cls, input):
        def check_scheme():
            try:
                return parse_url(input).scheme in {'http', 'https'}
            except Exception as e:
                return False
        if  type(input) is not str or not check_scheme():
            cls.raise_exc(input)
        return input

    @classmethod
    def name(cls, input):
        if not re.match(cls.VNREGEX, input):
            print('Invalid name provided.', file=sys.stderr)
            print(cls.VNREGEX_TEXT, file=sys.stderr)
            cls.raise_exc(input, msg=cls.VNREGEX_TEXT)
        return input


'''
runid(self, prop_path, config_value, purpose, visible):
        m = re.match(r"^[a-zA-Z0-9\-_]{3,30}$", config_value)
'''