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
import collections

class _DataEntity(collections.Mapping):
    _MANDATORY = set()
    _DEFAULT = set()
    _REFDICT = dict()

def _init(self, freeze=False, **kwargs):
    vars(self)['__freeze'] = freeze
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
        raise AttributeError("{} object does not have an attribute with name: {}. Allowed: {}".format(self.__class__.__name__, name, self._REFDICT.keys()))

def _sattr(self, name, value):
    if vars(self)['__freeze']:
        raise Exception(">>{}<< object is an immutable data entity (freeze is True). It does not support attribute assignment after object creation. You tried assigning value >>{}<< for attr/key >>{}<<.".format(self.__class__.__name__, value, name))
    else:
        if name in self._REFDICT:
            self._REFDICT[name] = value
        else:
            raise AttributeError("{} object does not have an attribute with name: {}. Allowed: {}".format(self.__class__.__name__, name, self._REFDICT.keys()))


def _as_dict(self, *, remove=None, remove_none=True):
    d = dict({k:v for k,v in vars(self).items() if not k.startswith('__')})
    if remove_none:
        d = {k:v for k,v in d.items() if v is not None}

    if remove is None:
        remove = set()
    elif type(remove) in {set, dict, list, tuple}:
        remove = set([i for i in remove])
    else:
        remove = {str(remove)}

    return {k:v for k,v in d.items() if k not in remove}

def _str(self):
    return "{klass}({attrs})".format(
        klass = self.__class__.__name__,
        attrs = ", ".join("{}={}".format(k,v) for k,v in self.as_dict().items())
    )

def _iter(self, *, remove=None, remove_none=True):
    return iter(self.as_dict(remove=remove, remove_none=remove_none))

def _getitem(self, k):
    return getattr(self, k)

def _setitem(self, k, v):
    return setattr(self, k, v)

def _delitem(self, name):
    raise Exception(">>{}<< object is a data entity. It does not support attribute/item deletion after object creation. You tried deleting value for >>{}<<. To get a dictionary representation without some attributes, call its as_dict() method with remove and/or remove_none arguments.".format(self.__class__.__name__, name))

def _len(self):
    return len(self.as_dict())

def _size(self, *, remove=None, remove_none=True):
    return len(self.as_dict(remove=remove, remove_none=remove_none))

def _items(self, *, remove=None, remove_none=True):
    return self.as_dict(remove=remove, remove_none=remove_none).items()

def _keys(self, *, remove=None, remove_none=True):
    return tuple(self.as_dict(remove=remove, remove_none=remove_none).keys())

def data_entity(entity_name, *attrs, bases=tuple(), **attrs_with_defaults):
    '''
        Create a new Data Entity class with provided name and attributes.

        Check :ref:`data_entity` documentation for various use cases.

        Arguments:
            entity_name: The class name for this new Data Entity type.
            *attrs: Arbitrary names for Python attributes to be associated with objects of this entity.

        Keyword Arguments:
            bases: Base data entities for this entity. Can be a string or tuple or list.
            **attrs_with_defaults: Arbitrary attributes to be associated with objects of this entity, with the defaults that are provided.

        Note:
            You can create objects of newly created data entity just like a normal Python class.

            .. code-block:: python

                Person = data_entity("Person", "name age")
                person = Person(name="SomeName", age=21)

        Note:
            The defaults that are provided can be any of the following:
                * Any Python Object
                * A Python callable
                * Arjuna `generator`
                * Arjuna `composite`

        Note:
            Data entity objects behave like Python dictionaries. 

            So you can retrieve an attribute value as:

                .. code-block:: python
                
                    entity.attr
                    # or
                    entity['attr']

            Following dict-like operations are valid too. The key difference to note is that in these operations that attributes that have None value are excluded unlike a Python dictionary.

                .. code-block:: python

                    entity.keys()
                    entity.items()
                    **entity # Unpacking of key-values

                    # Iterating on keys
                    for attr in entity:
                        pass

                    # Iterating on key-value pairs
                    for attr, value in entity.items():
                        pass

            To retain keys/attrs corresponding to None values, you can provide **remove_none=False** as argument:

                .. code-block:: python

                    entity.keys(remove_none=False)
                    entity.items(remove_none=False)
                    **entity # Unpacking of key-values

                    # Iterating on keys
                    for attr in entity.keys(remove_none=False):
                        pass

                    # Iterating on key-value pairs
                    for attr, value in entity.items(remove_none=False):
                        pass

            Also note that because len() in Python is not flexible to allow for the above, you can use **size** method:

                .. code-block:: python

                    len(entity) # Will ignore attrs with None value
                    entity.size() # Will ignore attrs with None value
                    entity.size(remove_none=False) # Includes attrs with None value

            All above mentioned methods also accept **remove** argument to explicitly exclude one or more attributes by name.

                .. code-block:: python

                    entity.keys(remove='some_key')
                    entity.keys(remove={'some_key1', 'some_key2'})

                    entity.items(remove='some_key')
                    entity.items(remove={'some_key1', 'some_key2'})

                    entity.size(remove='some_key')                 
                    entity.size(remove={'some_key1', 'some_key2'})

        Note:
            When you provide one or more bases, the overriding order is B1 -> B2 -> B3 ..... -> This Entity.

            At each stage of this chain, you can

                - Add one or more mandatory attributes.
                - Add one or more optional attributes
                - Make an optional attribute in base entity as mandatory.
                - Make a mandatory attribute as optional by assigning a default value.
                - Change the default for an existing default attribute to something else.

        Note:
            Delete operation is disllowed on the data entity because it corresponds to attribute deletion. Use **as_dict()** method for representation that has one or more keys removed.

                .. code-block:: python

                    # Raises exception
                    del entity['some_attr']

        Note:
            You can make an object of a data entity IMMUTABLE by passing **freeze=True** argument.

                .. code-block:: python

                    person = Person(name="SomeName", age=21, freeze=True)
                    # Raises Exception
                    person.age = 25

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
    namespace['__setattr__'] = _sattr
    namespace['as_dict'] = _as_dict
    namespace['__str__'] = _str
    namespace['__iter__'] = _iter
    namespace['__len__'] = _len
    namespace['__getitem__'] = _getitem
    namespace['__delitem__'] = _delitem
    namespace['__setitem__'] = _setitem
    namespace['keys'] = _keys
    namespace['items'] = _items
    namespace['size'] = _size
    return type(entity_name, (_DataEntity,), namespace)
