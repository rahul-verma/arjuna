from enum import Enum

def repr_dict(d, replace_value_enum=False):
    def format_key(k):
        if isinstance(k, Enum):
            return k.name.lower()
        elif type(k) is str:
            return k.lower()
        else:
            return k

    def format_value(v):
        if isinstance(v, Enum):
            if replace_value_enum:
                return v.name.lower()
            else:
                return v
        else:
            return v
    return "{" + ", ".join(["{}={}".format(format_key(k), format_value(v)) for k,v in d.items()]) + "}"