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

import logging
import os
import sys
import types
import inspect
import functools

from arjuna.core.utils.obj_utils import get_class_for_method

class _InvokerFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, "invoker"):
            record.invoker = '<no_trace>'
        if hasattr(record, "config"):
            if hasattr(record, "contexts"):
                if not record.contexts.intersection(record.config.value("log.allowed.contexts")):
                    return False

        return True

class Logger:

    def __init__(self, ref_config):
        self.__ref_config = ref_config
        self.__add_trace_level()
        self.__logger = None
        self.__load()

    def __load(self):
        from arjuna.tpi.enums import ArjunaOption
        dl = logging.getLevelName(self.__ref_config.value(ArjunaOption.LOG_CONSOLE_LEVEL).name) # logging.getLevelName(
        log_dir = self.__ref_config.value(ArjunaOption.LOG_DIR)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        fl = logging.getLevelName(self.__ref_config.value(ArjunaOption.LOG_FILE_LEVEL).name)
        fname = "arjuna.log"
        lpath = os.path.join(log_dir, fname)

        logger = logging.getLogger("arjuna")
        logger.addFilter(_InvokerFilter())
        logger.setLevel(logging.TRACE)
        ch = logging.StreamHandler(sys.stdout)
        ch.flush = sys.stdout.flush
        ch.setLevel(dl)
        fh = logging.FileHandler(lpath, "w", 'utf-8')
        fh.setLevel(fl)
        #f_fmt = logging.Formatter(u'[%(levelname)5s]\t%(asctime)s\t%(pathname)s::%(module)s.%(funcName)s:%(lineno)d\t%(message)s')
        f_fmt = logging.Formatter(u'[%(levelname)7s]\t%(asctime)s\t%(invoker)s\t%(message)s')
        c_fmt = logging.Formatter(u'[LOG] %(message)s')
        ch.setFormatter(c_fmt)
        fh.setFormatter(f_fmt)
        logger.addHandler(ch)
        logger.addHandler(fh)

        self.__logger = logger

    def __add_trace_level(self):
        logging.TRACE = logging.DEBUG - 1
        logging.addLevelName(logging.TRACE, "TRACE")
        def trace(self, message, *args, **kws):
            if self.isEnabledFor(logging.TRACE):
                # Yes, logger takes its '*args' as 'args'.
                self._log(logging.TRACE, message, args, **kws)
        logging.Logger.trace = trace

    @property
    def arjuna_logger(self):
        return self.__logger

prop_dict_msg = {
    "fget": ("(Getting Property)","", " Returning: {}"),
    "fset": ("(Setting Property)", ":: Args: {}, Kwargs: {}.", ""),
    "fdel": ("(Deleting Property)","", ""),
}

def  __func_wrapper(func, level, *vargs, static=False, prop=False, prop_type="fget", **kwargs):
    import arjuna
    from arjuna import log_error
    log_call = getattr(arjuna, "log_{}".format(level.strip().lower()))
    name = func.__name__
    qualname = func.__qualname__
    if name != qualname and not static:
        pvargs = vargs[1:]
    else:
        pvargs = vargs

    if prop:
        msg_1 = prop_dict_msg[prop_type][0]
        msg_2 = prop_dict_msg[prop_type][1].format(pvargs, kwargs)
        log_call("{} {}{}".format(qualname, msg_1, msg_2))
    else:
        log_call("{}:: Started with args {} and kwargs {}.".format(qualname, pvargs, kwargs))
    ret = None
    try:
        ret = func(*vargs, **kwargs)
    except Exception as e:
        import traceback
        log_error("{}:: Exception: {}. Trace: {}".format(qualname, e, traceback.format_exc()))
        raise
    else:
        if prop:
            msg_1 = prop_dict_msg[prop_type][0]
            msg_3 = prop_dict_msg[prop_type][2].format(ret)
            log_call("{}:: Finished.{}".format(qualname, msg_3, msg_3))
        else:
            log_call("{}:: Finished. Returning: {}".format(qualname, ret))
        return ret

def __track_func(level="debug", static=False, prop=False, prop_type="fget"):

    def dec(func):
        fname = func.__name__
        if prop is True:
            if not hasattr(func, "_wrapped"):
                func._wrapped = True
            elif func._wrapped:
                return func
        @functools.wraps(func)
        def inner(*vargs, **kwargs):
            return __func_wrapper(func, level, *vargs, static=static, prop=prop, prop_type=prop_type, **kwargs)
        return inner

    return dec

def __wrap_methods(cls, level, *args, **kwargs):
    for attr_name, attr in vars(cls).items():
        if type(attr) is types.FunctionType:
            setattr(cls, attr_name, __track_func(level)(attr))
        elif isinstance(attr, classmethod):
            setattr(cls, attr_name, classmethod(__track_func(level)(attr.__func__)))
        elif isinstance(attr, staticmethod):
            setattr(cls, attr_name, staticmethod(__track_func(level, static=True)(attr.__func__)))
    return cls(*args, **kwargs)

def __track_class(level):

    def deco(cls):
        @functools.wraps(cls)
        def class_wrapper(*args, **kwargs):
            return __wrap_methods(cls, level, *args, **kwargs)
        return class_wrapper

    return deco

def track(level="not_set"):

    kallable = None
    kallable_type = None
    non_arg_track = False

    if inspect.isclass(level) or inspect.isfunction(level) or isinstance(level, classmethod) or isinstance(level, staticmethod) or isinstance(level, property):
        kallable = level
        non_arg_track = True
        level = "debug"
        if inspect.isclass(kallable):
            return __track_class(level)(kallable)
        elif inspect.isfunction(kallable):
            return __track_func(level)(kallable)
        elif isinstance(kallable, classmethod):
            return classmethod(__track_func(level)(kallable.__func__))
        elif isinstance(kallable, staticmethod):
            return staticmethod(__track_func(level, static=True)(kallable.__func__))
        elif isinstance(kallable, property):
            return property(
                kallable.fget and __track_func(level, prop=True, prop_type="fget")(kallable.fget) or None,
                kallable.fset and __track_func(level, prop=True, prop_type="fset")(kallable.fset) or None,
                kallable.fdel and __track_func(level, prop=True, prop_type="fdel")(kallable.fdel) or None,
            )
        else:
            raise Exception("track decorator is meant for class/method/function only.")    
    else:
        level = level is not None and level or "debug"

    def deco(kallable):
        if inspect.isclass(kallable):
            return __track_class(level)(kallable)
        elif inspect.isfunction(kallable) or inspect.ismethod(kallable):
            return __track_func(level)(kallable)
        elif isinstance(kallable, classmethod):
            return classmethod(__track_func(level)(kallable.__func__))
        elif isinstance(kallable, staticmethod):
            return staticmethod(__track_func(level, static=True)(kallable.__func__))
        elif isinstance(kallable, property):
            return property(
                kallable.fget and __track_func(level, prop=True, prop_type="fget")(kallable.fget) or None,
                kallable.fset and __track_func(level, prop=True, prop_type="fset")(kallable.fset) or None,
                kallable.fdel and __track_func(level, prop=True, prop_type="fdel")(kallable.fdel) or None,
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