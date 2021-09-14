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

import uuid
from mimesis import locales as Locales
from mimesis import Text as MimesisText
from .number import Number

class Text:

    @classmethod
    def ustr(cls, *, prefix: str=None, maxlen: int=None, minlen: int=None, delim:str="-", strict=False) -> str:
        '''
            Generate a unique UUID string.
            If minlen/maxlen are specified in a manner that leads to uuid truncation, uniqueness is not enforced.
            Base string length is prefix length + delim length + 36 (length of uuid4)
            Different arguments tweak the length of generated string by appending uuid one or more times fully or partially.
            
            Keyword Arguments:
                prefix: (Optional) prefix to be added to the generated UUID string.
                minlen: (Optional) Minimum length of the retuned string (inclusive of prefix + delim). Default is base string length.
                maxlen: (Optional) Maximum length of the retuned string (inclusive of prefix + delim). Should be greater than minlen. Default is calculated as:
                    * if minlen > half of base string length, then default maxlen is 2 * minlen 
                    * if minlen <  half of base string length, then default maxlen is base string length

                delim: (Optional) Delimiter between prefix and generated string. Default is "-". Ignored if prefix is not specified.
                strict: (Optional) If True uniqueness of string is enforced which means full generated uuid must be used atleast once. This means length of generated string must be >= base string length, else an exception is thrown.
            Returns:
                A string that is unique for current session.
        '''
        if maxlen is not None and minlen is not None:
            if maxlen < minlen:
                raise Exception("maxlen must be greater than minlen for Random.ustr call")

        prefix = prefix and prefix + delim or ""
        gen_str = uuid.uuid4()
        base_str = prefix + str(gen_str)

        if strict:
            if minlen is not None and minlen < len(base_str):
                minlen = len(base_str)
            if maxlen is not None and maxlen < len(base_str):
                raise Exception("In strict mode the maxlen can not be less than length of prefix + delim + 36 (len of uuid). Generated string: >>{}<< (length={}). Specified maxlen: {}".format(base_str, len(base_str), maxlen))

        target_len = len(base_str)
        if minlen is not None and maxlen is not None:
            target_len = Number.int(begin=minlen, end=maxlen)
        elif minlen is not None:
            if minlen < 0.5 * len(base_str):
                target_len = Number.int(begin=minlen, end=len(base_str))
            else:
                target_len = Number.int(begin=minlen, end=2 * minlen)
        elif maxlen is not None:
            if maxlen <= len(base_str):
                target_len = maxlen
            else:
                target_len = Number.int(begin=len(base_str), end=maxlen)

        multiplier = (target_len // 36) + (target_len % 36 > 0 and 1 or 0)
        base_str = prefix + multiplier * str(gen_str)

        return base_str[:target_len]

    @classmethod
    def fixed_length_str(cls, *, length) -> str:
        '''
            Generate a fixed length string

            Keyword Arguments:
                length: Number of chracters in generated number.

            Returns:
                A generated fixed length string

            Note:
                A number of minimum length 1 is always generated.
        '''
        return cls.ustr(minlen=length, maxlen=length)[:length]

    @classmethod
    def sentence(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a sentence

            Keyword Arguments:
                locale: (Optional) locale for generating sentence

            Returns:
                A generated sentence
        '''
        return MimesisText(locale).sentence()

    @classmethod
    def alphabet(cls, *, locale=Locales.EN, lower_case=False):
        '''
            Generate a random integer.

            Keyword Arguments:
                locale: (Optional) Locale for data
                lower_case: (inclusive) If true lower case alphabet is returned where applicable.
            Returns:
                A list of alphabet characters.
        '''
        return MimesisText(locale).alphabet(lower_case=lower_case)

    @classmethod
    def answer(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a random answer.

            Keyword Arguments:
                locale: (Optional) Locale for data
        '''
        return MimesisText(locale).answer()

    @classmethod
    def level(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a random level for danger etc.

            Keyword Arguments:
                locale: (Optional) Locale for data
        '''
        return MimesisText(locale).level()

    @classmethod
    def quote(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a random quote.

            Keyword Arguments:
                locale: (Optional) Locale for data
        '''
        return MimesisText(locale).quote()

    @classmethod
    def word(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a random word.

            Keyword Arguments:
                locale: (Optional) Locale for data
        '''
        return MimesisText(locale).word()

    @classmethod
    def swear_word(cls, *, locale=Locales.EN) -> str:
        '''
            Generate a random swear word.

            Keyword Arguments:
                locale: (Optional) Locale for data
        '''
        return MimesisText(locale).swear_word()

    @classmethod
    def words(cls, *, locale=Locales.EN, count=5): # -> list[str]: Readthedocs has max version 3.8, this can be used 3.9 onwards
        '''
            Generate a random word.

            Keyword Arguments:
                locale: (Optional) Locale for data
                count: Number of words. Default is 5.
        '''
        return MimesisText(locale).words(count=count)