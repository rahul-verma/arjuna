# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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
Data Generator

This module contains classes and functions that generate data.
'''

import uuid
import random
from mimesis import Person
from mimesis import Address
from mimesis import locales
from mimesis import Text

Locales = locales

class Random:
    '''
        Provides methods to create random strings and numbers of different kinds.
    '''

    @classmethod
    def ustr(cls, *, prefix: str=None) -> str:
        '''
            Generate a unique UUID string

            Keyword Arguments:
                prefix: (Optional) prefix to be added to the generated UUID string.

            Returns:
                A string that is unique for current session.
        '''
        prefix = prefix and prefix + "-" or ""
        return "{}{}".format(prefix, uuid.uuid4())

    @classmethod
    def first_name(cls, *, locale=Locales.EN):
        '''
            Generate a first name.

            Keyword Arguments:
                locale: (Optional) locale for generating first name

            Returns:
                A generated first name
        '''
        return Person(locale).first_name()

    @classmethod
    def last_name(cls, *, locale=Locales.EN):
        '''
            Generate a last name.

            Keyword Arguments:
                locale: (Optional) locale for generating last name

            Returns:
                A generated last name
        '''
        return Person(locale).last_name()

    @classmethod
    def phone(cls, *, locale=Locales.EN):
        '''
            Generate a phone number.

            Keyword Arguments:
                locale: (Optional) locale for generating phone number

            Returns:
                A generated phone number
        '''
        return Person(locale).telephone()

    @classmethod
    def email(cls, *, locale=Locales.EN):
        '''
            Generate an email address.

            Keyword Arguments:
                locale: (Optional) locale for generating email address

            Returns:
                A generated email address
        '''
        return Person(locale).email()

    @classmethod
    def street_name(cls, *, locale=Locales.EN):
        '''
            Generate a street name

            Keyword Arguments:
                locale: (Optional) locale for generating street name

            Returns:
                A generated street name
        '''
        return Address(locale).street_name()

    @classmethod
    def street_number(cls, *, locale=Locales.EN):
        '''
            Generate a street number

            Keyword Arguments:
                locale: (Optional) locale for generating street number

            Returns:
                A generated street number
        '''
        return Address(locale).street_number()

    @classmethod
    def house_number(cls, *, locale=Locales.EN):
        '''
            Generate a house number

            Keyword Arguments:
                locale: (Optional) locale for generating house number

            Returns:
                A generated house number
        '''
        return cls.street_number(locale=locale)

    @classmethod
    def postal_code(cls, *, locale=Locales.EN):
        '''
            Generate a postal code

            Keyword Arguments:
                locale: (Optional) locale for generating postal code

            Returns:
                A generated postal code
        '''
        return Address(locale).postal_code()

    @classmethod
    def city(cls, *, locale=Locales.EN):
        '''
            Generate a city name.

            Keyword Arguments:
                locale: (Optional) locale for generating city name

            Returns:
                A generated city name
        '''
        return Address(locale).city()

    @classmethod
    def country(cls, *, locale=Locales.EN):
        '''
            Generate a country name

            Keyword Arguments:
                locale: (Optional) locale for generating country name

            Returns:
                A generated country name
        '''
        return Address(locale).country()

    @classmethod
    def sentence(cls, *, locale=Locales.EN):
        '''
            Generate a sentence

            Keyword Arguments:
                locale: (Optional) locale for generating sentence

            Returns:
                A generated sentence
        '''
        return Text(locale).sentence()

    @classmethod
    def fixed_length_number(cls, *, length):
        '''
            Generate a fixed length number

            Keyword Arguments:
                length: Number of digits in generated number.

            Returns:
                A generated fixed length number
        '''
        arr0 = [str(random.randint(1,9))]
        arr = [str(random.randint(0,9)) for i in range(length-1)]
        arr0.extend(arr)
        return "".join(arr0)
        
