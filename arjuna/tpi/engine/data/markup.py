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

from arjuna.engine.data.source import *
from arjuna.engine.data.factory import *
from arjuna.tpi.enums import *
from arjuna.core.utils import obj_utils
from arjuna.engine.data.factory import *

class _DataMarkUp:
    pass

class _DataRecord(_DataMarkUp):

    from arjuna.engine.data.source import SingleDataRecordSource
    def __init__(self, *vargs, **kwargs):
        super().__init__()
        if not vargs and not kwargs:
            raise Exception("No data provided in Data")
        self.__record = DataRecord(*vargs, **kwargs)

    def build(self):
        source = SingleDataRecordSource(self.__record)
        return source

    def get_record(self):
        return self.__record

record = _DataRecord

class _DataRecords(_DataMarkUp):
    from arjuna.engine.data.source import DataArrayDataSource
    def __init__(self, *records):
        super().__init__()
        for i in records:
            if not isinstance(i, record):
                raise Exception("Items in records() must be instances of record.")
        self.records = [i.get_record() for i in records]

    def build(self):
        source = DataArrayDataSource(self.records)
        return source

records = _DataRecords

class _DataFunc(_DataMarkUp):
    def __init__(self, func, *vargs, **kwargs):
        super().__init__()
        if not obj_utils.callable(func):
            raise Exception("Argument provided to data_function should be a function object.")
        elif not obj_utils.is_function(func):
            raise Exception("Argument for data_function should be a function object which does not exist inside a class.")
        self.func = func
        self.vargs = vargs
        self.kwargs = kwargs

    def build(self):
        return DataFunctionDataSource(self.func, *self.vargs, **self.kwargs)

data_function = _DataFunc

class _DataClass(_DataMarkUp):
    def __init__(self, dsclass, *vargs, **kwargs):
        super().__init__()
        if not isinstance(type(dsclass), type):
            raise Exception("Data Class expects dsclass to be a class.")
        self.dsclass = dsclass
        self.vargs = vargs
        self.kwargs = kwargs

    def build(self):
        return DataClassDataSource(self.dsclass, *self.vargs, **self.kwargs)

data_class = _DataClass


class _DataFile(_DataMarkUp):
    def __init__(self, path=None, delimiter="\t"):
        super().__init__()
        self.path = path
        self.delimiter = delimiter

    def build(self):
        source = create_file_data_source(self.path, delimiter=self.delimiter)
        return source

data_file = _DataFile

class _MultiDataSource(_DataMarkUp):
    def __init__(self, *dsources):
        super().__init__()
        if not dsources:
            raise Exception("You must provide atleast one data source as argument for many_data_sources")
        for dsource in dsources:
            if not isinstance(dsource, _DataMarkUp):
                raise Exception("All arguments of many_data_sources must be data sources.")
        self.dsource_defs = dsources

    def build(self):
        return MultiDataSource(self.dsource_defs)

many_data_sources = _MultiDataSource


