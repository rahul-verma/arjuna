from arjuna.core.adv.types import CIStringDict
from arjuna.configure.impl.validator import Validator

class WithX:

    def __init__(self, xdict={}):
        self.__xdict = CIStringDict()
        for k,v in xdict.items():
            try:
                self.__xdict[Validator.arjuna_name(k)] = {"wtype" : xdict[k]["wtype"].strip().upper(), "value" : xdict[k]["value"].strip()}
            except Exception as e:
                print(e)
                print(xdict)
                raise Exception(f"Invalid WithX name >>{k}<<.")

    def has_locator(self, name):
        return name in self.__xdict

    def format_args(self, name, *vargs, **kwargs):
        if not self.has_locator(name):
            raise Exception("No WithX locator with name {} found.".format(name))
        fmt = self.__xdict[name]
        try:
            return fmt["wtype"], fmt["value"].format(*vargs, **kwargs)
        except Exception as e:
            from arjuna import Arjuna
            Arjuna.get_logger().error(f"Error in processing withx {name} : {fmt} for vargs {vargs} and kwargs {kwargs}")
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
        return self.format_args(name, *vargs, **kwargs)
        

    