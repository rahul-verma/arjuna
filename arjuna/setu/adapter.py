import abc
from arjuna.client.core.action import *

class Handler(metaclass=abc.ABCMeta):

    @classmethod
    def _pop_arg(cls, json_args_dict, key, optional=False):
        try:
            value = json_args_dict[key]
            del json_args_dict[key]
            return value
        except Exception as e:
            if optional: 
                return None
            else: 
                raise Exception("Input value for {} not found in JSON args: {}.".format(key, json_args_dict))

    @classmethod
    def get_element_setuid(cls, json_dict):
        return cls._pop_arg(json_dict, "elementSetuId")

    @classmethod
    def get_text_blob_setu_id(cls, json_dict):
        return cls._pop_arg(json_dict, "textBlobSetuId")

    @classmethod
    def get_config_setuid(cls, json_dict):
        return cls._pop_arg(json_dict, "configSetuId")

    @classmethod
    def get_extended_config(cls, json_dict):
        return cls._pop_arg(json_dict, "extendedConfig", optional=True)

    @classmethod
    def get_orig_gui_component_type(cls, json_dict):
        value = cls._pop_arg(json_dict, "origGuiComponentType", optional=True)
        if value is None:
            return ""
        else:
            return value + "_"

    @classmethod
    def process_action_type(cls, action_type, json_dict):
        if action_type == GuiAutoActionType.DEFINE:
            return action_type.name + "_" + cls._pop_arg(json_dict, "defGuiComponentType")
        else:
            return action_type.name

        