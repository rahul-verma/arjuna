import copy
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.configure.validator import Validator

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
        try:
            if fmt["wtype"] in {'ATTR', 'FATTR'}:
                for k,v in fmt["wvalue"].items():
                    fmt["wvalue"][k] = v.format(**kwargs)
                return fmt["wtype"], fmt["wvalue"]
            else:
                return fmt["wtype"], fmt["wvalue"].format(*vargs, **kwargs)
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
        

    