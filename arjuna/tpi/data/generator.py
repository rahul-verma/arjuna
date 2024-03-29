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


from mimesis import locales

'''
Data Generator

This module contains classes and functions that generate data.
'''

from arjuna.engine.data.generator.text import Text
from arjuna.engine.data.generator.number import Number
from arjuna.engine.data.generator.person import Person
from arjuna.engine.data.generator.address import Address
from arjuna.engine.data.generator.entity import Entity
from arjuna.engine.data.generator.color import Color
from arjuna.engine.data.generator.file import File

class _gen:
    pass

class processor:
    '''
        Processes data by calling the provided callable with provided arguments.

        Arguments:
            callable: The callable to be called in processing.
            *args: Arbitrary positional args to be passed to the callable.

        Keyword Arguments:
            **kwargs: Arbitrary keyword arguments to tbe passed to the callable.
    '''

    def __init__(self, callable, *args, **kwargs):
        self.__callble = callable
        self.__args = args
        self.__kwargs = kwargs

    def process(self, data):
        '''
            Processes data in the provided data object by calling the callable with arguments provided in constructor.

            Arguments:
                data: Data object
        '''
        if type(self.__callble) is str:
            return getattr(data, self.__callble)(*self.__args, **self.__kwargs)
        else:
            return self.__callble(data_iterator, *self.__args, **self.__kwargs)  

class composer:
    '''
        Combines data in an iterable by calling the provided callable with provided arguments.

        Arguments:
            callable: The callable to be called in composing.
            *args: Arbitrary positional args to be passed to the callable.

        Keyword Arguments:
            **kwargs: Arbitrary keyword arguments to tbe passed to the callable.
    '''

    def __init__(self, callable, *args, **kwargs):
        self.__callble = callable
        self.__args = args
        self.__kwargs = kwargs

    def compose(self, data_iter):
        '''
            Combine data in the provided iterable by calling the callable with arguments provided in constructor.

            Arguments:
                data_iter: Data iterable
        '''
        return self.__callble(data_iter, *self.__args, **self.__kwargs)  

def _same(in_data):
    return in_data

class generator(_gen):
    '''
        Generate data by calling the provided callable with provided arguments.

        Arguments:
            callable: The callable to be called in composing. By default, same generated object is returned.
            *args: Arbitrary positional args to be passed to the callable.

        Keyword Arguments:
            processor: This callable is called after data is generated by passing generated data as argument. Useful for data transformation of any kind. If its type is string, it is assumed to be a method of the data which the data callable generated.
            **kwargs: Arbitrary keyword arguments to tbe passed to the callable.
    '''

    def __init__(self, callable, *args, processor=_same, **kwargs):
        self.__callble = callable
        self.__args = args
        self.__kwargs = kwargs
        self.__processor = processor

    def generate(self):
        '''
            Generate data by calling the callable with arguments provided in constructor.

            After generation the coverter callable is called with this data before returning the data.
        '''
        data = self.__callble(*self.__args, **self.__kwargs)
        if type(self.__processor) is str:
            return getattr(data, self.__processor)()
        elif isinstance(self.__processor, processor):
            return self.__processor.process(data)
        else:
            return self.__processor(data)

class composite(_gen):
    '''
        Composite Data Generator.

        Generate data by composing the output of all generators, callables or static data.

        Arguments:
            *generators_or_data: Arbitrary generators, functions or static data objects.

        Keyword Arguments:
            composer: This callable is called after data sequence is generated by passing generated data sequence as argument. Useful for data transformation of any kind.
    '''

    def __init__(self, *generators_or_data, composer=_same):
        self.__generators_or_data = generators_or_data
        self.__composer = composer

    def generate(self):
        '''
            Generate data by composing the output of all generators, callables or static data.
            
            The composer callable is called after data sequence is generated by passing generated data sequence as argument. Useful for data transformation of any kind.
        '''
        out = list()
        for gen_or_data in self.__generators_or_data:
            if hasattr(gen_or_data, '__call__'):
                out.append(gen_or_data())
            elif isinstance(gen_or_data, generator):
                out.append(gen_or_data.generate())
            else:
                out.append(gen_or_data)

        if isinstance(self.__composer, composer):
            return self.__composer.compose(out)
        else:
            return self.__composer(out)

class DataLocale:
    '''
        Data Locale object.

        When this object is passed where relevant to Random class methods, it localizes the data generated.

        To create a specific locale object, you can use the dot notation.

        .. code-block:: python

            locale.en
            locale.fr

        For list of supported locales, check :ref:`suppored_data_locales`. You also use the following code to get all supported locale names:

        .. code-block:: python

            locale.supported
    '''

    __SUPPORTED = {
        'cs': 'Czech', 
        'da': 'Danish', 
        'de': 'German', 
        'de_at': 'Austrian German', 
        'de_ch': 'Swiss German', 
        'el': 'Greek', 
        'en': 'English', 
        'en_gb': 'British English', 
        'en_au': 'Australian English', 
        'en_ca': 'Canadian English', 
        'es': 'Spanish', 
        'es_mx': 'Mexican Spanish', 
        'et': 'Estonian', 
        'fa': 'Farsi', 
        'fi': 'Finnish', 
        'fr': 'French', 
        'hu': 'Hungarian', 
        'is': 'Icelandic', 
        'it': 'Italian', 
        'ja': 'Japanese', 
        'kk': 'Kazakh', 
        'ko': 'Korean', 
        'nl': 'Dutch', 
        'nl_be': 'Belgium Dutch', 
        'no': 'Norwegian', 
        'pl': 'Polish', 
        'pt': 'Portuguese', 
        'pt_br': 'Brazilian Portuguese', 
        'ru': 'Russian', 
        'sv': 'Swedish', 
        'tr': 'Turkish', 
        'uk': 'Ukrainian', 
        'zh': 'Chinese'
    }

    _SINGLE_OBJ = {

    }

    def __getattr__(self, name):
        if name.lower() in self.__SUPPORTED:
            if name not in self._SINGLE_OBJ:
                self._SINGLE_OBJ[name] = getattr(locales, name.upper())
            return self._SINGLE_OBJ[name]
        else:
            raise Exception(f"{name} is not a support locale name for Random class methods. Allowed: {self.__SUPPORTED}")

    @property
    def supported(self):
        import copy
        return copy.deepcopy(self.__SUPPORTED)


class __RandomMetaClass(type):

    @property
    def locale(cls):
        return DataLocale()


class Random(metaclass=__RandomMetaClass):
    '''
        Provides methods to create random strings and numbers of different kinds.
    '''

    # Text
    ustr = Text.ustr
    fixed_length_str = Text.fixed_length_str
    sentence = Text.sentence
    alphabet = Text.alphabet

    # Number
    int = Number.int
    fixed_length_number = Number.fixed_length_number

    # Person
    first_name = Person.first_name
    last_name = Person.last_name
    name = Person.name
    phone = Person.phone
    email = Person.email

    # Address
    street_number = Address.street_number
    street_name = Address.street_name
    house_number = Address.house_number
    postal_code = Address.postal_code
    city = Address.city
    country = Address.country

    # Color
    color = Color.color
    rgb_color = Color.rgb_color
    hex_color = Color.hex_color

    # # File
    # mp3 = File.mp3
    # aac = File.aac
    # zip = File.zip
    # gzip = File.gzip
    # pdf = File.pdf
    # docx = File.docx
    # xlsx = File.xlsx
    # pptx = File.pptx
    # gif = File.gif
    # png = File.png
    # jpg = File.jpg
    # mov = File.mov
    # mp4 = File.mp4

    # Entities
    person = Entity.person
    address = Entity.address




        


    