# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast

safe_eval = ast.literal_eval

def convert_yaml_obj_to_content(jval):
    def handle_str_val(in_val):
        if in_val.lower().strip() == "null":
            out_val = "null"
        else:
            # The string could be a variable name. With spaces, it will be treated as Python statement.
            if in_val in locals() or in_val in globals():
                out_val = in_val
            else:
                try:
                    out_val = safe_eval(in_val)
                except (NameError, SyntaxError, ValueError): # The string is evaluated as a variable name or Python statement
                    out_val = jval
        return out_val

    if type(jval) is dict:
        # This is needed if e.g. "1" is a string and not to be treated as a number. In this case type: str should be coded.
        if "value" in jval:
            raw_value = jval["value"]
            if "type" in jval:
                jtype = jval["type"].lower().strip()
                allowed_set = {"str", "dict", "list", "int", "float", "bool"}
                if jtype in allowed_set:
                    jval = eval(jtype)(jval["value"])
                else:
                    raise Exception("type can be specified only as one of {}".format(allowed_set))
            elif type(raw_value) is str:
                jval = handle_str_val(raw_value)
            else:
                jval = raw_value
        else:
            jval = jval
    elif type(jval) is str:
        jval = handle_str_val(jval)
    else:
        jval = jval

    return jval