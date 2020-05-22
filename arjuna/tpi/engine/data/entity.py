# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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


def _init(self, **kwargs):
    wrong_args = False
    provided_set = kwargs.keys()
    mandatory_args_missing = self._MANDATORY - provided_set
    if mandatory_args_missing:
        wrong_args = True
    default_arg_diff = kwargs.keys() - self._REFDICT.keys()
    if default_arg_diff:
        wrong_args = True

    if wrong_args:
        mandatory_args_missing = mandatory_args_missing and f" Missing mandatory args: {mandatory_args_missing}. Must: {self._MANDATORY}" or ""
        default_arg_diff = default_arg_diff and f" Unexpected default args: {default_arg_diff}. Allowed: {self._DEFAULT}." or ""
        raise Exception(f"Wrong arguments.{mandatory_args_missing}{default_arg_diff}")

    vars(self).update(self._REFDICT)
    vars(self).update(kwargs)


def _attr(self, name):
    if name in self._REFDICT:
        return self._REFDICT[name]
    else:
        raise AttributeError("{} object does not have an attribute with name: {}.".format(self.__class__.__name__, name))

def _as_dict(self, remove_none=False):
    d = dict(vars(self))
    if remove_none:
        return {k:v for k,v in d.items() if v is not None}
    else:
        return d

def data_entity(entity_name, *attrs, **attrs_with_defaults):
    for attr in attrs:
        if type(attr) is not str:
            raise Exception(f"Data Entity fields must be valid Python name strings. Got: {attr}")
    namespace = dict()
    namespace['_MANDATORY'] = set(attrs)
    namespace['_DEFAULT'] = set(attrs_with_defaults.keys())
    namespace['_REFDICT'] = dict()
    namespace['_REFDICT'].update({f: None for f in attrs})
    namespace['_REFDICT'].update(attrs_with_defaults)
    namespace['__init__'] = _init
    namespace['__getattr__'] = _attr
    namespace['as_dict'] = _as_dict
    return type(entity_name, tuple(), namespace)


DataEntity = data_entity