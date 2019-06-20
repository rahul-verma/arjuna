'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import types
import copy
import pprint

from arjuna.lib.adv.types import *
from arjuna.lib.adv.proxy import ROProxy
from arjuna.lib.types.descriptors import *
from arjuna.unitee.validation.steps import Steps
from arjuna.lib.config import InternalTestContext

SCALARS = {int, float, str, bool}

class SingleObjectVars(CIStringDict):

    def __setitem__(self, key, value):
        if type(value) not in SCALARS:
            raise Exception("Single Vars dictionaries can only contain scalars ({}) as values.".format(SCALARS))
        super().__setitem__(key, value)

    def merge_with_parent(self, parent_vars):
        _d = SingleObjectVars()
        _d.update(parent_vars)
        _d.update(self)
        self.update(_d)

class evars:
    def __init__(self, **kwargs):
        self.__dict = kwargs
        
    def get_dict(self):
        return self.__dict

    def __str__(self):
        return pprint.pformat(self.__dict)


class MultiVars:

    def __init__(self, child_count, **kwargs):
        self.__svars = [SingleObjectVars() for i in range(child_count)]
        for k,v in kwargs.items():
            bl = self.__balance(child_count, v)
            for i in range(child_count):
                self.__svars[i][k] = bl[i]

    def __balance(self, count, l):
        if not ListTupleOrSet.check(l):
            l = [l]
        for i in l:
            if type(i) not in SCALARS:
                raise Exception("Multi Vars dictionaries can only contain list of scalars ({}) as values.".format(SCALARS))
        if len(l) == count:
            return l
        elif len(l) > count:
            return l[:count]
        else:
            return l + [l[-1] for i in range(count - len(l))]

    def __str__(self):
        return pprint.pformat(self.__svars)


class TagSet:

    def __init__(self, *vargs):
        self.__set = {str(i).lower() for i in vargs}

    def __fv(self, item):
        return str(item).lower()

    def __contains__(self, item):
        return self.__fv(item) in self.__set

    def update(self, items):
        for item in items:
            self.__set.add(self.__fv(item))

    def __iter__(self):
        return iter(self.__set)

    def is_empty(self):
        return len(self.__set) == 0

    def __str__(self):
        return str(self.__set)

tags = TagSet
bugs = TagSet


class DataRef:
    pass


class DataRefs:
    def __init__(self, **kwargs):
        self._drefs = SingleObjectVars()
        for k,v in kwargs:
            if not isinstance(v, DataRef):
                raise Exception("The argumens of DataRefs must be name=DataRef object.")
            else:
                self.add(k, v)

    def __getattr__(self, item):
        return self._drefs[item]

    def __setattr__(self, key, value):
        if key != "_drefs":
            vars(self)['_drefs'][key] = value
        else:
            vars(self)['_drefs'] = value

    def add(self, name, dref):
        self._drefs[name] = dref

    def __str__(self):
        return pprint.pformat(self._drefs, indent=4)


class TestInfo:
    def __init__(self, meta):
        self.meta = meta
        self.props = CIStringDict()

    def set_props(self, sdict):
        for k,v in sdict.items():
            if k != "kwargs":
                self.props[k] = v
            else:
                for i,j in v.items():
                    self.props[i] = j

    def freeze(self):
        self.meta = types.MappingProxyType(self.meta)
        self.props = types.MappingProxyType(self.props)

    def __str__(self):
        return '''Meta\n{}\nProps\n{}\n'''.format(str(self.meta), str(self.props))

    def clone(self):
        info = self.__class__()
        info.meta = self.meta.clone()
        info.props = ROProxy(self.props.clone())
        return info


class SessionInfo(TestInfo):
    def __init__(self):
        super().__init__(CIStringDict({
            "name": "-"
        }))


class StageInfo(TestInfo):
    def __init__(self):
        super().__init__(CIStringDict({
            "name": "-"
        }))


class GroupInfo(TestInfo):
    def __init__(self):
        super().__init__(CIStringDict({
            "name": "-",
            "slot": "-"
        }))


class ModuleInfo(TestInfo):
    def __init__(self):
        super().__init__(CIStringDict({
            "pkg": "-",
            "name": "-",
            "qname": "-",
            "slot" : "-"
        }))


class FunctionInfo(TestInfo):
    def __init__(self):
        super().__init__(CIStringDict({
            "name": "-",
            "qname": "-"
        }))

# class RODataRecord:
#
#     def __init__(self, drec):
#         if drec:
#             self.indexed = tuple(drec.indexed)
#             self.named = types.MappingProxyType(drec.named)
#         else:
#             self.indexed = None
#             self.named = None


class AllInfo:

    def __init__(self):
        self.session = None
        self.stage = None
        self.group = None
        self.module = None
        self.function = None
        self.object_type = None
        self.test_num = None

    def create_ro_wrapper(self):
        info = AllInfo()
        info.session = ROProxy(self.session)
        info.stage = ROProxy(self.stage)
        info.group = ROProxy(self.group)
        info.module = ROProxy(self.module)
        info.function = ROProxy(self.function)
        info.object_type = self.object_type
        info.test_num = self.test_num
        return ROProxy(info)

    def clone(self):
        info = AllInfo()
        info.session = self.session and self.session.clone() or SessionInfo()
        info.stage = self.stage and self.stage.clone() or StageInfo()
        info.group = self.group and self.group.clone() or GroupInfo()
        info.module = self.module and self.module.clone() or ModuleInfo()
        info.function = self.function and self.function.clone() or FunctionInfo()
        info.object_type = self.object_type
        info.test_num = self.test_num
        return info


class State:

    steps = Steps


class Data:

    def __init__(self):
        self.record = None


class TestVars:

    def __init__(self):
        self.info = AllInfo()
        self.context = None
        self.evars = SingleObjectVars()
        self.runtime = OnceOnlyKeyCIStringDict()
        self.tags = tags() # return frozen set
        self.bugs = tags()  # return frozen set
        self.data = None

    def clone(self):
        nvars = TestVars()
        if self.context is not None:
            nvars.context = self.context.clone()
        else:
            nvars.context = None
        nvars.info = self.info.clone()
        nvars.evars = SingleObjectVars({i:j for i,j in self.evars.items()})
        nvars.tags = TagSet(*{i for i in self.tags})
        nvars.bugs = TagSet(*{i for i in self.bugs})
        nvars.data = Data() #RODataRecord For .pos it should be a tuple, for .map immutable dict
        nvars.runtime = self.runtime.clone()
        return nvars

    def create_utvars(self):
        class UTVars:
            def __init__(self, tvars):
                # RO
                self.info = tvars.info.create_ro_wrapper()
                self.tags = frozenset(tvars.tags)
                self.bugs = frozenset(tvars.bugs)
                self.context = tvars.context.clone_for_user()
                # R/W
                self.evars = tvars.evars
                self.runtime = tvars.runtime
                # data
                self.data = ROProxy(tvars.data)
                # steps
                self.steps = Steps

        return ROProxy(UTVars(self))

    def __str__(self):
        out = ""
        names = list(vars(self).keys())
        names.sort()
        for name in names:
            out += "Contents of: " + name + "\n"
            out += str(vars(self)[name]) + "\n"
        return out

