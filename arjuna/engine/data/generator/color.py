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
from mimesis import locales as Locales
from mimesis import Text

class Color:

    @classmethod
    def color(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a random color string.

            Keyword Arguments:
                locale: (Optional) locale for generating street name

            Returns:
                A generated color
        '''
        return Text(locale).color()

    @classmethod
    def hex_color(cls) -> str:
        '''
            Generate a hex color code.

            Returns:
                A generated hex color code string
        '''
        return Text().hex_color()

    @classmethod
    def rgb_color(cls) -> tuple:
        '''
            Generate an rgb color tuple.

            Returns:
                RGB tuple
        '''
        return Text().rgb_color()

