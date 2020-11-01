import copy
import re
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.configure.validator import Validator

def _format(target, repl_dict):

    def get_global_value(in_str):
        from arjuna import C, L, R
        gtype, query = in_str.split(".", 1)
        gtype = gtype.upper()
        return locals()[gtype](query)

    pattern = r"\$(\s*[\w\.]*?\s*)\$"
    fmt_target = target.replace("\{", "__LB__").replace("}", "__RB__")

    # Find params
    matches = re.findall(pattern, fmt_target)
    
    for match in matches:
        names_set = None
        target = "${}$".format(match)
        processed_name = match.lower().strip()
        repl_value = None
        if processed_name.startswith("c.") or processed_name.startswith("l.") or processed_name.startswith("r."):
            repl_value = get_global_value(processed_name)
        else:
            if processed_name not in repl_dict:
                continue
            repl_value = repl_dict[processed_name]

        fmt_target = fmt_target.replace(target, str(repl_value))
        

    fmt_target = fmt_target.replace("__LB__", "{").replace("__RB__", "}")
    return fmt_target

class WithX:

    def __init__(self, xdict={}):
        self.__xdict = CIStringDict()
        for k,v in xdict.items():
            try:
                self.__xdict[Validator.name(k)] = {"wtype" : xdict[k]["wtype"].strip().upper(), "wvalue" : xdict[k]["wvalue"]}
            except Exception as e:
                raise Exception(f"Invalid WithX entry for name >>{k}<<.")

    def has_locator(self, name):
        return name in self.__xdict

    def format_args(self, name, vargs, kwargs):
        if not self.has_locator(name):
            raise Exception("No WithX locator with name {} found.".format(name))

        # Critical to create a copy
        fmt = copy.deepcopy(self.__xdict[name])
        repl_dict = {k.lower():v for k,v in kwargs.items()}
        try:
            if fmt["wtype"] in {'ATTR', 'FATTR', 'NODE', 'BNODE', 'FNODE'}:
                out = dict()
                for k,v in fmt["wvalue"].items():
                    out[_format(k, repl_dict)] = _format(v, repl_dict)
                    #out[k.format(**kwargs)] = v.format(**kwargs)
                return fmt["wtype"], out
            else:
                return fmt["wtype"], _format(["wvalue"], repl_dict) #fmt["wvalue"].format(*vargs, **kwargs)
        except Exception as e:
            from arjuna import log_error
            log_error(f"Error in processing withx {name} : {fmt} for vargs {vargs} and kwargs {kwargs}")
            raise

    def format(self, name, loc_obj):
        vargs = None
        kwargs = None
        if type(loc_obj) is str:
            vargs = [loc_obj]
            kwargs = dict()
        elif type(loc_obj) in {list, tuple}:
            vargs = loc_obj
            kwargs = dict()
        elif type(loc_obj) is dict:
            vargs = []
            kwargs = loc_obj
        return self.format_args(name, vargs, kwargs)
        

    