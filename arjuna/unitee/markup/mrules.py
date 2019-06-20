from arjuna.unitee.enums import *

built_in_prop_type = {
    BuiltInProp.ID : str,
    BuiltInProp.PRIORITY : int,
    BuiltInProp.THREADS : int,
    BuiltInProp.NAME : str,
    BuiltInProp.AUTHOR : str,
    BuiltInProp.IDEA : str,
    BuiltInProp.UNSTABLE : bool,
    BuiltInProp.COMPONENT : str,
    BuiltInProp.APP_VERSION : str,
}

def validate_built_in_props(props):
    for k,v in props.items():
        if is_builtin_prop(k.upper()):
            expected_type = built_in_prop_type[BuiltInProp[k.upper()]]
            actual_type = type(v)
            if v is not None and actual_type is not expected_type:
                raise Exception("Built-in property {} should of type {}. Found {} of type {}".format(
                    k,
                    expected_type,
                    v,
                    actual_type
                ))

def get_value_type(built_in_prop_name):
    return built_in_prop_type[BuiltInProp[built_in_prop_name.upper()]]

def is_builtin_prop(name):
    return name.upper() in BuiltInProp.__members__