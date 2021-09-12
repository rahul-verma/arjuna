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
from mimesis import Person as MimesisPerson

class Person:

    @classmethod
    def first_name(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a first name.

            Keyword Arguments:
                locale: (Optional) locale for generating first name

            Returns:
                A generated first name
        '''
        return MimesisPerson(locale).first_name()

    @classmethod
    def last_name(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a last name.

            Keyword Arguments:
                locale: (Optional) locale for generating last name

            Returns:
                A generated last name
        '''
        return MimesisPerson(locale).last_name()

    @classmethod
    def name(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a full name (first name and last name).

            Keyword Arguments:
                locale: (Optional) locale for generating phone number

            Returns:
                A generated full name
        '''
        return "{} {}".format(cls.first_name(locale=locale), cls.last_name(locale=locale))

    @classmethod
    def phone(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a phone number.

            Keyword Arguments:
                locale: (Optional) locale for generating phone number

            Returns:
                A generated phone number
        '''
        return MimesisPerson(locale).telephone()

    @classmethod
    def email(cls, *, locale=Locales.EN, name=None, domain=None) -> str:
        '''
            Generate an email address.

            Keyword Arguments:
                locale: (Optional) locale for generating email address
                name: (Optional) If provided, then email address is created as <provided name>@<generated domain>
                domain: (Optional) If provided, then email address is created as <generated name>@<provided domain>

            Returns:
                A generated email address
        '''
        gname, gdomain = MimesisPerson(locale).email().rsplit("@", 1)
        name = name is not None and name or gname
        domain = domain is not None and domain or gdomain
        return f"{name}@{domain}"