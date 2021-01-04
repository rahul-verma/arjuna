import copy
import re
import pickle
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.configure.validator import Validator

def _format(target, vargs, repl_dict):

    def get_global_value(in_str):
        from arjuna import C, L, R
        gtype, query = in_str.split(".", 1)
        gtype = gtype.upper()
        return locals()[gtype](query)

    do_eval = False
    if type(target) is not str:
        do_eval = True
        target = str(target)

    pos_pattern = r"(\$\s*\$)"
    named_pattern = r"\$(\s*[\w\.]+?\s*)\$"
    fmt_target = target.replace("{", "__LB__").replace("}", "__RB__")

    # Find params
    pos_matches = re.findall(pos_pattern, fmt_target)
    named_matches = re.findall(named_pattern, fmt_target)

    if pos_matches and named_matches:
        for match in named_matches:
            match = match.lower().strip()
            if not match.startswith("c.") and not match.startswith("l.") and not match.startswith("r."):
                raise Exception("You can not use positional $$ placeholders and named $<name>$ placholders together in a withx locator definition (except those with C./L./R. prefixes to fetch global values. Wrong withx definition: " + target)

    if pos_matches:
        if not vargs:
            vargs = tuple()    
        if len(pos_matches) != len(vargs):
            raise Exception("Number of positional arguments supplied to format withx locator do not match number of $$ placeholders. Placeholders: {}. Positional args: {}. Wrong usage of withx locator: {}".format(len(pos_matches), vargs, target))

        for i,match in enumerate(pos_matches):
            fmt_target = fmt_target.replace(match, "{}")

        fmt_target = fmt_target.format(*vargs)
        
    for match in named_matches:
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
    if do_eval:
        fmt_target = eval(fmt_target)
    return fmt_target

class WithX:

    def __init__(self, xdict={}):
        def process_value(wtype, wvalue):
            if wtype in {'ATTR', 'FATTR', 'BATTR', 'EATTR'}: #:, 'NODE', 'BNODE', 'FNODE'}:
                if len(wvalue) > 1:
                    raise Exception("attr/fattr/battr/eattr specification should contain only a single key value pair for attribute name and value. Wrong withx definition found wtype: {} with value {}".format(wtype, wvalue))
                name = list(wvalue.keys())[0]
                value = list(wvalue.values())[0]
                return {'name' : name, 'value' : value}
            else:
                return wvalue

        self.__xdict = CIStringDict()
        for k,v in xdict.items():
            try:
                wname = Validator.name(k)
                wtype = xdict[k]["wtype"].strip().upper()
                wvalue = xdict[k]["wvalue"]
                self.__xdict[wname] = {"wtype" : wtype, "wvalue" : process_value(wtype, wvalue)}
            except Exception as e:
                raise Exception(f"Invalid WithX entry for name >>{k}<<. {e}")

    def has_locator(self, name):
        return name in self.__xdict

    def format_args(self, name, vargs, kwargs):
        if not self.has_locator(name):
            raise Exception("No WithX locator with name {} found.".format(name))

        # Critical to create a copy
        fmt = copy.deepcopy(self.__xdict[name])
        if kwargs:
            repl_dict = {k.lower():v for k,v in kwargs.items()}
        else:
            repl_dict = {}
        try:

            return fmt["wtype"], _format(fmt["wvalue"], vargs, repl_dict)
            # if fmt["wtype"] in {'ATTR', 'FATTR', 'BATTR', 'EATTR', 'NODE', 'BNODE', 'FNODE'}:
            #     out = dict()
            #     for k,v in fmt["wvalue"].items():
            #         if type(v) in {list, tuple}:
            #             out[_format(k, repl_dict)] = [_format(v_entry, repl_dict) for v_entry in v]
            #         else:
            #             out[_format(k, repl_dict)] = _format(v, repl_dict)
            #         #out[k.format(**kwargs)] = v.format(**kwargs)
            #     return fmt["wtype"], out
            # else:
            #     return fmt["wtype"], _format(["wvalue"], repl_dict) #fmt["wvalue"].format(*vargs, **kwargs)
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