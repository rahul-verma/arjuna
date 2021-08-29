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

##########################################################
# Raised and consumed by internal implementation of Arjuna
##########################################################

import re
from arjuna.tpi.data.entity import _DataEntity

def arj_format_str(target, vargs, repl_dict):
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

    def get_value_from_container(name, *, container=None):
        if container is None:
            parts = name.split(".", 1)
            if len(parts) == 1:
                # It is reference directly to an object and if present could have been resolved before this logic hits.
                return "__NOTFOUND"
            container, name = parts

        name_parts = re.split(r'([\.\[])', name, 1) # Will return single element list or 3 part list: name, delim, rest
        if len(name_parts) == 1:
            name, delim, rest = name, "", ""
        else:
            name, delim, rest = name_parts

        try:
            container = repl_dict[container]
            if type(container) is dict:
                first_obj = container[name]
            elif isinstance(type(container), _DataEntity):
                first_obj = getattr(container, name)
            if delim == "":
                return first_obj
            else:
                return eval(f"first_obj{delim}{rest}")
        except Exception as e:
            return "__NOTFOUND"                 
        
    for match in named_matches:
        names_set = None
        target = "${}$".format(match)
        processed_name = match.lower().strip()
        repl_value = None
        if processed_name.startswith("c.") or processed_name.startswith("l.") or processed_name.startswith("r."):
            repl_value = get_global_value(processed_name)
        elif processed_name.startswith("data."):
            processed_name = processed_name.split(".")[1]
            if 'data' in repl_dict:
                temp_val = get_value_from_container(processed_name, container="data")
                if temp_val == "__NOTFOUND":
                    continue
                else:
                    repl_value = temp_val
            else:
                continue
        else:
            if processed_name not in repl_dict:
                # Try a container and dynamic logic like a.b.c or a.b[3]
                temp_val = get_value_from_container(processed_name)
                if temp_val != "__NOTFOUND":
                    repl_value = temp_val
                else:
                    if 'data' in repl_dict:
                        temp_val = get_value_from_container(processed_name, container="data")
                        if temp_val == "__NOTFOUND":
                            continue
                        else:
                            repl_value = temp_val
                    else:
                        continue
            else:
                repl_value = repl_dict[processed_name]

        fmt_target = fmt_target.replace(target, str(repl_value))

    fmt_target = fmt_target.replace("__LB__", "{").replace("__RB__", "}")
    if do_eval:
        fmt_target = eval(fmt_target)
    return fmt_target

def arj_convert(content):

        if content is None:
            return content

        if type(content) is str and content == "":
            return content

        from json import JSONEncoder, dumps, loads
        from arjuna.tpi.parser.yaml import YamlDict, YamlList
        from arjuna.tpi.parser.json import JsonDict, JsonList
        from arjuna.tpi.data.entity import _DataEntity
        from arjuna.tpi.helper.arjtype import CIStringDict

        class _CustomEncoder(JSONEncoder):
            def default(self, o):
                if isinstance(o, YamlDict) or isinstance(o, YamlList) or isinstance(o, JsonList) or isinstance(o, JsonDict):
                    return o.raw_object
                elif isinstance(o, _DataEntity):
                    return o.as_dict()
                elif isinstance(o, CIStringDict):
                    return o.store
                return JSONEncoder.default(self, o)

        if type(content) is tuple:
            content = list(content)

        # if content:
        if isinstance(content, JsonList) or isinstance(content, JsonDict) or isinstance(content, YamlList) or isinstance(content, YamlDict):
            content = content.raw_object
        elif isinstance(content, _DataEntity):
            content = content.as_dict()
        elif isinstance(content, CIStringDict):
            content = content.store
        elif content == "null":
            content = None
        else:
            if not content:
                if content is not None:
                    content = str(content)

        content = dumps(content, cls=_CustomEncoder, indent=2)

        if content != "":
            return loads(content)
        else:
            return ""