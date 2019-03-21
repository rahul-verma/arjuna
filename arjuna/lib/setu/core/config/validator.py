import inspect
import os
import copy
from urllib3.util import parse_url
from arjuna.tpi.enums import *

class ConfigValidator:

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
            cls.raise_exc(input)
        return input

    @classmethod
    def int(cls, input):
        if type(input) is not int:
            cls.raise_exc(input)
        return input

    @classmethod
    def float(cls, input):
        if type(input) is not float:
            cls.raise_exc(input)
        return input

    @classmethod
    def absolute_dir_path(cls, input):
        if type(input) is not str:
            cls.raise_exc(input)
        elif not os.path.isabs(input) or not os.path.isdir(input):
            cls.raise_exc(input)
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
    def mobile_os(cls, input):
        try:
            return MobileOsName[input.upper()]
        except:
            cls.raise_exc(input)

    @classmethod
    def positive_int(cls, input):
        if type(input) is not int or input <= 1:
            cls.raise_exc(input)
        return input

    @classmethod
    def positive_float(cls, input):
        if type(input) is not float or input < 0.1:
            cls.raise_exc(input)
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

