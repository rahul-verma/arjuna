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
Data Driven Testing Markup

Provides data source builder classes that can be provided to drive_with argument of @test decorator.

The names of the classes have been kept in lower case for aesthetic purpose of the @test decorator.
'''

from arjuna.engine.data.source import *
from arjuna.engine.data.factory import *
from arjuna.tpi.constant import *
from arjuna.core.constant import *
from arjuna.core.utils import obj_utils
from arjuna.engine.data.factory import *

class _DataMarkUp:
    pass

class record(_DataMarkUp):
    '''
        Data Record Data Source

        Args:
            vargs: Any number of objects
            *kwargs: Arbitrary keywrod arguments
    '''

    from arjuna.engine.data.source import SingleDataRecordSource
    def __init__(self, *vargs, **kwargs):
        super().__init__()
        self.__vargs = vargs
        self.__kwargs = kwargs
        if not vargs and not kwargs:
            raise Exception("No data provided in Data") 

    def build(self, context="Test") -> 'DataSource':
        '''
            Create corresponding DataSource
        '''
        return SingleDataRecordSource(self.get_record(context=context), context=context)

    def get_record(self, *, context="Test"):
        return DataRecord(context=context, *self.__vargs, **self.__kwargs)

class records(_DataMarkUp):
    '''
        Multiple Data Record Data Source

        Args:
            *records: Any number of record objects
    '''

    from arjuna.engine.data.source import DataArrayDataSource
    def __init__(self, *records):
        super().__init__()
        for i in records:
            if not isinstance(i, record):
                raise Exception("Items in records() must be instances of record.")
        self.__records = records

    def build(self, context="Test") -> 'DataSource':
        '''
            Create corresponding DataSource
        '''
        return DataArrayDataSource(self.get_records(context=context), context=context)

    def get_records(self, *, context="Test"):
        return [i.get_record(context=context) for i in self.__records]

class data_function(_DataMarkUp):
    '''
        Data Function/Generator Data Source

        Args:
            func: Function object to be called.
            vargs: Any number of objects to be passed to function when calling it.
            *kwargs: Arbitrary keywrod arguments to be passed to function when calling it.
    '''

    def __init__(self, func, *vargs, **kwargs):
        super().__init__()
        if not obj_utils.callable(func):
            raise Exception("Argument provided to data_function should be a function object.")
        elif not obj_utils.is_function(func):
            raise Exception("Argument for data_function should be a function object which does not exist inside a class.")
        self.func = func
        self.vargs = vargs
        self.kwargs = kwargs

    def build(self, context="Test") -> 'DataSource':
        '''
            Create corresponding DataSource
        '''
        return DataFunctionDataSource(self.func, *self.vargs, context=context, **self.kwargs)


class data_class(_DataMarkUp):
    '''
        Data Class Data Source

        Args:
            dsclass: Class to be instantiated
            vargs: Any number of objects for instantiating the class.
            *kwargs: Arbitrary keywrod arguments  for instantiating the class.
    '''

    def __init__(self, dsclass, *vargs, **kwargs):
        super().__init__()
        if not isinstance(type(dsclass), type):
            raise Exception("Data Class expects dsclass to be a class.")
        self.dsclass = dsclass
        self.vargs = vargs
        self.kwargs = kwargs

    def build(self, context="Test") -> 'DataSource':
        '''
            Create corresponding DataSource
        '''
        return DataClassDataSource(self.dsclass, *self.vargs, context=context, **self.kwargs)


class data_file(_DataMarkUp):
    '''
        Data File Data Source

        Args:
            path: Path of the file
            
        Keyword Arguments:
            delimiter: (Optional) Delimiter to be used for text files. Default is tab (\t)
    '''
    def __init__(self, path=None, *, delimiter="\t"):
        super().__init__()
        self.path = path
        self.delimiter = delimiter

    def build(self, context="Test") -> 'DataSource':
        '''
            Create corresponding DataSource
        '''
        source = create_file_data_source(self.path, delimiter=self.delimiter, context=context)
        return source


class many_data_sources(_DataMarkUp):
    '''
        Multiple Data Source

        Args:
            *dsources: Any Arjuna Data Source
            
        Keyword Arguments:
            delimiter: (Optional) Delimiter to be used for text files. Default is tab (\t)
    '''
    def __init__(self, *dsources):
        super().__init__()
        if not dsources:
            raise Exception("You must provide atleast one data source as argument for many_data_sources")
        for dsource in dsources:
            if not isinstance(dsource, _DataMarkUp):
                raise Exception("All arguments of many_data_sources must be data sources.")
        self.dsource_defs = dsources

    def build(self, context="Test") -> 'DataSource':
        '''
            Create corresponding DataSource
        '''
        return MultiDataSource(self.dsource_defs, context=context)



