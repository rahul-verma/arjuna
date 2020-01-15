import time
import inspect

from arjuna.tpi import Arjuna

class HardCoded:

    @classmethod
    def __get_invoker(cls):
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

    @classmethod
    def __log(cls, invoker, why, seconds):
        Arjuna.get_logger().warn("Hardcoded sleep executed for {} seconds by {}. Reason by author: {}".format(seconds, invoker, why))

    @classmethod
    def sleep(cls, why, seconds):
        time.sleep(seconds)
        cls.__log(cls.__get_invoker(), why, seconds)