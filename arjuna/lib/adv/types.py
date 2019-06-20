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

import pprint
from collections import OrderedDict

class CIStringDict:

    def __init__(self, d={}, ordered=False):
        if ordered:
            self.__store = OrderedDict()
        else:
            self.__store = {}
        self.update(d)

    def __getitem__(self, key):
        return self.__store[key.lower()]

    def __setitem__(self, key, value):
        self.__store[key.lower()] = value

    def __delitem__(self, key):
        del self.__store[key.lower()]

    def update(self, d):
        if not d: return
        for k,v in d.items():
            self[k.lower()] = v

    def has_key(self, key):
        return key.lower() in self.__store

    def __getattr__(self, attr):
        return getattr(self.__store, attr)

    def __len__(self):
        return len(self.__store.keys())

    def __str__(self):
        if not self.__store:
            return "<empty>"

        parts = []
        keys = list(self.__store.keys())
        keys.sort()
        for k in keys:
            if self.__store[k] is not None:
                parts.append("[{}] {}".format(k, self.__store[k]))
        return "\n".join(parts)

    def __iter__(self):
        return iter(self.__store)

    def clone(self):
        return CIStringDict(self.__store)

    def items(self):
        return self.__store.items()

    def is_empty(self):
        return len(self.__store) == 0


class OnceOnlyKeyCIStringDict(CIStringDict):

    def __init__(self, d={}):
        super().__init__(d)

    def __setitem__(self, key, value):
        if self.has_key(key):
            raise Exception("You can not change the value once set.")
        super().__setitem__(key, value)

    def update(self, d):
        if not d: return
        as_dict = dict(d)
        for k in as_dict:
            self[k] = as_dict.get(k)

    def __iter__(self):
        return super().__iter__()

    def clone(self):
        return OnceOnlyKeyCIStringDict(self.items())