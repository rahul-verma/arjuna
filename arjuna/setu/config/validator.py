import inspect
import os
import re
import sys
from urllib3.util import parse_url
from arjuna.tpi.enums import *
from arjuna.lib.enums import *
from arjuna.unitee.enums import *
from arjuna.lib.types.constants import *

class ConfigValidator:
    VNREGEX = r'[a-z][a-z0-9]{2,29}'
    VNREGEX_TEXT = '''
    A Setu name must be a string of length 3-30 containing lower case letters, digits or _ (underscore).
    It must begin with a letter.
    '''

    @classmethod
    def raise_exc(cls, input):
        curframe = inspect.currentframe()
        callframe = inspect.getouterframes(curframe, 2)
        caller = callframe[1][3]
        raise Exception("{} is not {}".format(input, caller))

    @classmethod
    def str(cls, input):
        if type(input) is not str:
            cls.raise_exc(input)
        return input

    @classmethod
    def bool(cls, input):
        if type(input) is not bool:
            if type(input) is str:
                if input in TRUES:
                    return True
                elif input in FALSES:
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
        else:
            os.makedirs(input)
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
            return LoggingLevelEnum[input.upper()]
        except Exception as e:
            print(e)
            cls.raise_exc(input)

    @classmethod
    def str_list(cls, input):
        if type(input) is not list:
            cls.raise_exc(input)
        else:
            s = {type(i) for i in input}
            if s != {type("")}:
                cls.raise_exc(input)
        return input

    @classmethod
    def actor_mode(cls, input):
        try:
            return SetuActorMode[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def browser_name(cls, input):
        try:
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
    def active_reporter_list(cls, input):
        l = None
        if type(input) is str:
            l = [input]
        elif type(input) is list:
            l = input
        else:
            cls.raise_exc(input)
        try:
            return [ActiveReporterNames[i.upper()] for i in input]
        except:
            cls.raise_exc(input)

    @classmethod
    def deferred_reporter_list(cls, input):
        l = None
        if type(input) is str:
            l = [input]
        elif type(input) is list:
            l = input
        else:
            cls.raise_exc(input)
        try:
            return [DeferredReporterNames[i.upper()] for i in input]
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
                print(e)
                return False
        if  type(input) is not str or not check_scheme():
            cls.raise_exc(input)
        return input

    @classmethod
    def setu_name(cls, input):
        if not re.match(cls.VNREGEX, input):
            print('Invalid Setu name provided.', file=sys.stderr)
            print(cls.VNREGEX_TEXT, file=sys.stderr)
            cls.raise_exc(input)
        return input


'''
runid(self, prop_path, config_value, purpose, visible):
        m = re.match(r"^[a-zA-Z0-9\-_]{3,30}$", config_value)
'''