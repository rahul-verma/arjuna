import abc

class Handler(metaclass=abc.ABCMeta):

    @classmethod
    def _pop_arg(cls, json_args_dict, key, optional=False):
        try:
            value = json_args_dict[key]
            del json_args_dict[key]
            return value
        except Exception as e:
            print(e)
            if optional: 
                return None
            else: 
                raise Exception("Input value for {} not found in JSON args: {}.".format(key, json_args_dict))

    @classmethod
    def get_element_setuid(cls, json_dict):
        return cls._pop_arg(json_dict, "elementSetuId")

    @classmethod
    def get_config_setuid(cls, json_dict):
        return cls._pop_arg(json_dict, "configSetuId")

    @classmethod
    def get_extended_config(cls, json_dict):
        return cls._pop_arg(json_dict, "extendedConfig", optional=True)