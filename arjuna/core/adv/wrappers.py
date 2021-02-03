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


class ClassPassThrough:
    def __init__(self, klass, *cargs, **ckwargs):
        vars(self)['_o'] = klass(*cargs, **ckwargs)

    def __getattr__(self, item):
        if item in ['_o', '__lock__']:
            return vars(self)[item]
        else:
            return self.pass_through_get(item)

    def __setattr__(self, item, value):
        if item in ['_o', '__lock__']:
            vars(self)[item] = value
        else:
            self.pass_through_set(item, value)

    def pass_through_get(self, item):
        return getattr(self._o, item)

    def pass_through_set(self, item, value):
        return setattr(self._o, item, value)

    def __iter__(self):
        return iter(self._o)