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

'''
Arjuna Defined Types

These types are used for annotating functions, methods and return types.

In future, they could be used to enforce types. For the time being, the purpose is understandability and documentation.
'''
from typing import TypeVar
from arjuna.tpi.constant import ArjunaOption

ListOrTuple = TypeVar('ListOrTuple', list, tuple)
ListOrTupleOrStr = TypeVar('ListOrTupleOrStr', list, tuple, str)
ArjunaOptionOrStr = TypeVar('ArjunaOptionOrStr', ArjunaOption, str)