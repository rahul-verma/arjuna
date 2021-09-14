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