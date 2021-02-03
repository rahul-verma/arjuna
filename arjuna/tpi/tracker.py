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

from arjuna.engine.track import *

def track(level: str="debug"):
    '''
        Decorator to track a callable.

        You can track classes, methods, functions and properties using this decorator.

        Arjuna tracks the following and logs it as per **log_*** function chosen as per provided level. Default is debug.
            - Begin of call and arguments passed to the call.
            - End of the call with return value
            - Exception raised if any

        Keywrod Arguments:
            callable: Callable that is decorated.
            level: (Optional) A string representing a Logging Level (trace/debug/info/warning/error/fatal). Default is debug.

        Note:
            When you decorate a class with @track, it automatically tracks its construction, all its methods including classmethods and staticmethods.

            Properties are not auto-tracked for a class.

            You can add @track decorator to a property. If you have a property setter, adding @track to it automatically also tracks the getter.

            You can selectively add decorators to methods in the class as well.

            @track also works for functions.
    '''

    kallable = None
    kallable_type = None
    non_arg_track = False

    if inspect.isclass(level) or inspect.isfunction(level) or isinstance(level, classmethod) or isinstance(level, staticmethod) or isinstance(level, property):
        kallable = level
        non_arg_track = True
        level = "debug"
        if inspect.isclass(kallable):
            return track_class(kallable, level)
        elif inspect.isfunction(kallable):
            return track_func(level)(kallable)
        elif isinstance(kallable, classmethod):
            return classmethod(track_func(level)(kallable.__func__))
        elif isinstance(kallable, staticmethod):
            return staticmethod(track_func(level, static=True)(kallable.__func__))
        elif isinstance(kallable, property):
            return property(
                kallable.fget and track_func(level, prop=True, prop_type="fget")(kallable.fget) or None,
                kallable.fset and track_func(level, prop=True, prop_type="fset")(kallable.fset) or None,
                kallable.fdel and track_func(level, prop=True, prop_type="fdel")(kallable.fdel) or None,
            )
        else:
            raise Exception("track decorator is meant for class/method/function only.")    
    else:
        level = level is not None and level or "debug"

    def deco(kallable):
        if inspect.isclass(kallable):
            return track_class(kallable, level)
        elif inspect.isfunction(kallable) or inspect.ismethod(kallable):
            return track_func(level)(kallable)
        elif isinstance(kallable, classmethod):
            return classmethod(track_func(level)(kallable.__func__))
        elif isinstance(kallable, staticmethod):
            return staticmethod(track_func(level, static=True)(kallable.__func__))
        elif isinstance(kallable, property):
            return property(
                kallable.fget and track_func(level, prop=True, prop_type="fget")(kallable.fget) or None,
                kallable.fset and track_func(level, prop=True, prop_type="fset")(kallable.fset) or None,
                kallable.fdel and track_func(level, prop=True, prop_type="fdel")(kallable.fdel) or None,
            )
    return deco  

'''
    def __load_console(self, dl, logger):
        class __console:
            lock = threading.RLock()

            def __init__(self):
                # self.lock = threading.RLock()
                self.separator = os.linesep
                self.log_display_level = dl
                self.logger = logger

            @sync_method('lock')
            def __log(self, message, err=False):
                if err:
                    mparts = message.replace(u"\r\n", u"--|--").replace(u"\n", u"--|--").split(u'--|--')
                    for mpart in mparts:
                        self.logger.error(mpart)
                else:
                    mparts = message.replace(u"\r\n", u"--|--").replace(u"\n", u"--|--").split(u'--|--')
                    for mpart in mparts:
                        self.logger.info(mpart)

            @sync_method('lock')
            def __print(self, message):
                print(message, end='', file=sys.stdout, flush=True)

            @sync_method('lock')
            def __eprint(self, message):
                print(message, end='', file=sys.stderr, flush=True)

            @sync_method('lock')
            def __println(self, message):
                print(message, file=sys.stdout, flush=True)

            @sync_method('lock')
            def __eprintln(self, message):
                print(message, file=sys.stderr, flush=True)

            @sync_method('lock')
            def __msg(self, *messages):
                return " ".join([str(m) for m in messages])

            @sync_method('lock')
            def display(self, *messages):
                message = self.__msg(*messages)
                should_print = self.__log(message)
                if should_print:
                    self.__println(message)

            @sync_method('lock')
            def display_error(self, *messages):
                message = self.__msg(*messages)
                should_print = self.__log(message, err=True)
                if should_print:
                    self.__eprintln(message)

            @sync_method('lock')
            def error_for_console(self, *messages):
                message = self.__msg(*messages)
                self.__eprintln(message)

            @sync_method('lock')
            def display_on_same_line(self, *messages):
                message = self.__msg(*messages)
                should_print = self.__log(message)
                if should_print:
                    self.__print(message)

            @sync_method('lock')
            def marker(self, length, symbol='-'):
                self.display(symbol * length)

            @sync_method('lock')
            def marker_error(self, length, symbol='-'):
                self.display_error(symbol * length)

            @sync_method('lock')
            def marker_on_same_line(self, length=40):
                self.display_on_same_line("-" * length)

            @sync_method('lock')
            def display_key_value(self, key, value):
                message = "%s %s".format(key, value)
                self.display(message)

            @sync_method('lock')
            def __get_formatted_key_value(self, key, value, left_padding):
                if not left_padding:
                    message = "| {:20s}| {}".format(key, value)
                else:
                    message = "| {}| {}".format(key.ljust(left_padding), value)
                return message

            @sync_method('lock')
            def __display_paddedKV(self, key, value, print_func, left_padding):
                print_func(self.__get_formatted_key_value(key, value, left_padding))

            @sync_method('lock')
            def display_padded_key_value(self, key, value, left_padding=None):
                self.__display_paddedKV(key, value, self.display, left_padding)

            @sync_method('lock')
            def display_padded_key_value_error(self, key, value, left_padding=None):
                self.__display_paddedKV(key, value, self.display_error, left_padding)

            @sync_method('lock')
            def display_exception_block(self, e, strace):
                self.marker_error(80)
                self.display_padded_key_value_error("Exception Type", e.__class__.__name__, 30)
                self.display_padded_key_value_error("Exception Message", str(e), 30)
                self.display_padded_key_value_exception_trace("Exception Trace", strace, 30)
                self.marker_error(80)

            def set_central_log_level(self, level):
                self.central_log_level = level

            @sync_method('lock')
            def display_multiline_key_value(self, key, value, left_padding=30):
                value = str(value)
                ctrace_parts = value.replace("\t", " ").replace("\r\n\r\n","\r\n").replace("\n\n","\n").split(sys_utils.get_line_separator())

                header = self.__get_formatted_key_value(key, ctrace_parts[0], left_padding)
                self.__log(header)
                # if should_print:
                #     self.error_for_console(header)

                for s in ctrace_parts[1:]:
                    message = self.__get_formatted_key_value("", s, left_padding)
                    self.__log(message)
                    # if should_print:
                    #     self.(message)

            display_padded_key_value_exception_trace = display_multiline_key_value
        self.__console = __console()
'''