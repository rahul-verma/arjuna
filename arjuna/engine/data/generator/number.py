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

import random

class Number:

    @classmethod
    def fixed_length_number(cls, *, length) -> int:
        '''
            Generate a fixed length number

            Keyword Arguments:
                length: Number of digits in generated number.

            Returns:
                A generated fixed length number

            Note:
                A number of minimum length 1 is always generated.
        '''
        arr0 = [str(random.randint(1,9))]
        arr = []
        if length >= 2:
            arr = [str(random.randint(0,9)) for i in range(length-1)]
        arr0.extend(arr)
        return int("".join(arr0))

    @classmethod
    def int(cls, *, end, begin=0) -> int:
        '''
            Generate a random integer.

            Keyword Arguments:
                end: (inclusive) upper limit for the integer
                begin: (inclusive) lower limit for the integer. Default is 0.

            Returns:
                A generated integer
        '''
        return random.randint(begin, end)
