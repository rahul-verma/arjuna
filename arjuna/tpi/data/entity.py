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

from .generator import _gen

class _DataEntity:
    _MANDATORY = set()
    _DEFAULT = set()
    _REFDICT = dict()

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
        allowed = set(self._REFDICT.keys())
        default_arg_diff = default_arg_diff and f" Unexpected args: {default_arg_diff}. Allowed: {allowed}." or ""
        raise Exception(f"Wrong arguments.{mandatory_args_missing}{default_arg_diff}")

    def update_gen_data(key, value):
        if hasattr(value, '__call__'):
            value = value()
        elif isinstance(value, _gen):
            value = value.generate()

        vars(self)[key] = value

    final_dict = dict()
    final_dict.update(self._REFDICT)
    final_dict.update(kwargs)    

    for k,v in final_dict.items():
        update_gen_data(k,v)

def _attr(self, name):
    if name in self._REFDICT:
        return self._REFDICT[name]
    else:
        raise AttributeError("{} object does not have an attribute with name: {}.".format(self.__class__.__name__, name))

def _as_dict(self, remove_none=True):
    d = dict(vars(self))
    if remove_none:
        return {k:v for k,v in d.items() if v is not None}
    else:
        return d

def _str(self):
    return "{klass}({attrs})".format(
        klass = self.__class__.__name__,
        attrs = ", ".join("{}={}".format(k,v) for k,v in self.as_dict().items())
    )

def _iter(self):
    return iter(self.as_dict())

def __getitem__(self, k):
    return getattr(self, k)

def data_entity(entity_name, *attrs, bases=tuple(), **attrs_with_defaults):
    '''
        Create a new Data Entity class with provided name and attributes.

        Arguments:
            entity_name: The class name for this new Data Entity type.
            *attrs: Arbitrary names for Python attributes to be associated with objects of this entity.

        Keyword Arguments:
            bases: Base data entities for this entity. Can be a string or tuple or list.
            **attrs_with_defaults: Arbitrary attributes to be associated with objects of this entity, with the defaults that are provided.

        Note:
            The defaults that are provided can be any of the following:
                * Any Python Object
                * A Python callable
                * Arjuna `generator`
                * Arjuna `composite`

        Note:
            When you provide one or more bases, the overriding order is B1 -> B2 -> B3 ..... -> This Entity.

            At each stage of this chain, you can

                - Add one or more mandatory attributes.
                - Add one or more optional attributes
                - Make an optional attribute in base entity as mandatory.
                - Make a mandatory attribute as optional by assigning a default value.
                - Change the default for an existing default attribute to something else.
    '''
    for attr in attrs:
        if type(attr) is not str:
            raise Exception(f"Data Entity fields must be valid Python name strings. Got: {attr}")

    final_attrs = []
    # In any multiple names in single string are provided like a namedtuple, added as individual names.
    for attr in attrs:
        final_attrs.extend(attr.split())

    if not set(final_attrs).isdisjoint(set(attrs_with_defaults.keys())):
        raise Exception("Mandatory attribute can not be assigned a default value. Evaluate usage for: {}".format(set(final_attrs).intersection(set(attrs_with_defaults.keys()))))

    namespace = dict()
    namespace['_MANDATORY'] = set()
    namespace['_DEFAULT'] = set()
    namespace['_REFDICT'] = dict()

    if type(bases) not in {list, tuple}:
        bases = (bases,)

    for base in bases:
        base_vars = vars(base)
        namespace['_MANDATORY'] = namespace['_MANDATORY'].union(base_vars['_MANDATORY'])
        # Remove these params from Defaults
        for attr in namespace['_DEFAULT'].intersection(namespace['_MANDATORY']):
            namespace['_DEFAULT'].remove(attr)

        namespace['_DEFAULT'] = namespace['_DEFAULT'].union(base_vars['_DEFAULT'])
        # Remove optional params from Mandatory
        for attr in namespace['_DEFAULT'].intersection(namespace['_MANDATORY']):
            namespace['_MANDATORY'].remove(attr)
        #namespace['_MANDATORY'].difference_update(namespace['_DEFAULT'])
        namespace['_REFDICT'].update(base_vars['_REFDICT'])

    namespace['_MANDATORY'] = namespace['_MANDATORY'].union(set(final_attrs))
    # Remove mandatory params from Defaults
    for attr in namespace['_DEFAULT'].intersection(namespace['_MANDATORY']):
        namespace['_DEFAULT'].remove(attr)
    namespace['_DEFAULT'] = namespace['_DEFAULT'].union(set(attrs_with_defaults.keys()))
    # Remove optional params from Mandatory
    for attr in namespace['_DEFAULT'].intersection(namespace['_MANDATORY']):
        namespace['_MANDATORY'].remove(attr)
    namespace['_REFDICT'].update({f: None for f in final_attrs})
    namespace['_REFDICT'].update(attrs_with_defaults)

    namespace['__init__'] = _init
    namespace['__getattr__'] = _attr
    namespace['as_dict'] = _as_dict
    namespace['__str__'] = _str
    namespace['__iter__'] = _iter
    return type(entity_name, (_DataEntity,), namespace)

