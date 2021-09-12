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

from mimesis import locales as Locales
from mimesis import Address as MimesisAddress

class Address:

    @classmethod
    def street_name(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a street name

            Keyword Arguments:
                locale: (Optional) locale for generating street name

            Returns:
                A generated street name
        '''
        return MimesisAddress(locale).street_name()

    @classmethod
    def street_number(cls, *, locale=Locales.EN, prefix="") -> str:
        '''
            Generate a street number

            Keyword Arguments:
                locale: (Optional) locale for generating street number
                prefix: (Optional) prefix to be added to the generated street number. Space is used as delimited between prefix and generated street number.

            Returns:
                A generated street number
        '''
        if prefix != "":
            prefix = f"{prefix} "
        return prefix + MimesisAddress(locale).street_number()

    @classmethod
    def house_number(cls, *, locale=Locales.EN, prefix="") -> str:
        '''
            Generate a house number

            Keyword Arguments:
                locale: (Optional) locale for generating house number
                prefix: (Optional) prefix to be added to the generated house number. Space is used as delimited between prefix and generated house number.

            Returns:
                A generated house number
        '''
        return cls.street_number(locale=locale, prefix=prefix)

    @classmethod
    def postal_code(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a postal code

            Keyword Arguments:
                locale: (Optional) locale for generating postal code

            Returns:
                A generated postal code
        '''
        return MimesisAddress(locale).postal_code()

    @classmethod
    def city(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a city name.

            Keyword Arguments:
                locale: (Optional) locale for generating city name

            Returns:
                A generated city name
        '''
        return MimesisAddress(locale).city()

    @classmethod
    def country(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a country name

            Keyword Arguments:
                locale: (Optional) locale for generating country name

            Returns:
                A generated country name
        '''
        return MimesisAddress(locale).country()
