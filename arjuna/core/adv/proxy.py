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

class ROProxy:
    def __init__(self, wrapped):
        vars(self)['__wrapped'] = wrapped

    def __getattr__(self, item):
        try:
            return getattr(vars(self)['__wrapped'], item)
        except AttributeError as e:
            raise Exception("Map does not contain attribute: >>{}<<".format(item))

    def __getitem__(self, item):
        try:
            return vars(self)['__wrapped'][item]
        except AttributeError as e:
            raise Exception("Map does not contain key: >>{}<<".format(item))

    def __setattr__(self, key, value):
        raise Exception("Read-Only Proxy does not support item assignment.")

    def __str__(self):
        return str(vars(self)['__wrapped'])

