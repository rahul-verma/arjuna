import copy
import re
import pickle
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.configure.validator import Validator
from arjuna.core.fmt import arj_format_str

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

            return fmt["wtype"], arj_format_str(fmt["wvalue"], vargs, repl_dict)
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