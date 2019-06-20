'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import abc
import threading
import types

from arjuna.lib.reader.excel import *
from arjuna.lib.reader.ini import *
from arjuna.lib.reader.textfile import *
from arjuna.lib.thread import decorators
from arjuna.unitee.ddt.record import *
from arjuna.unitee.exceptions import *
from arjuna.lib.utils import sys_utils


class DataSource(metaclass=abc.ABCMeta):

    def __init__(self):
        self.lock = threading.RLock()
        self.name = None
        self.ended = False

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    @decorators.sync_method('lock')
    def terminate(self):
        self.ended = True

    def is_terminated(self):
        return self.ended

    def validate(self):
        pass

    @decorators.sync_method('lock')
    def next(self):
        if self.is_terminated():
            raise DataSourceFinished()

        try:
            data_record = self.get_next()
            if not data_record:
                raise StopIteration()
            record = self.process(data_record)
            if self.should_exclude(record):
                return self.next()
            else:
                return record
        except StopIteration as e:
            raise DataSourceFinished("Records Finished.")
        except Exception as e:
            raise DataSourceFinished(
                "Problem happened in getting next record. No further records would be provided.")

    def process(self, data_record):
        return data_record

    @abc.abstractmethod
    def get_next(self):
        pass

    @abc.abstractmethod
    def should_exclude(self, data_record):
        return False


class FileDataSource(DataSource):
    def __init__(self):
        super().__init__()
        self.reader = None

    def _set_reader(self, reader):
        self.reader = reader

    def get_next(self):
        return self.reader.next()

    def should_exclude(self, data_record):
        return False


class DsvFileDataSource(FileDataSource):
    def __init__(self, path, delimiter="\t"):
        super().__init__()
        self.reader = FileLine2ArrayReader(path, delimiter)
        self.headers = self.reader.get_headers()

    def process(self, data_record):
        return DataRecord(**dict(zip(self.headers, data_record)))


class IniFileDataSource(FileDataSource):
    def __init__(self, path):
        super().__init__()
        if path.lower().endswith("ini"):
            self.reader = IniFile2MapReader(path)
        else:
            raise Exception("Unsupported file extension for Ini reading.")

    def process(self, data_record):
        return DataRecord(**data_record)


class ExcelFileDataSource(FileDataSource):
    def __init__(self, path):
        super().__init__()
        if path.lower().endswith("xls"):
            self.reader = ExcelRow2ArrayReader(path)
            self.headers = self.reader.get_headers()
        else:
            raise Exception("Unsupported file extension for Excel reading.")

    def get_next(self):
        return self.reader.next()

    def should_exclude(self, data_record):
        return data_record.named_values().get('exclude', 'n') == 'y'

    def process(self, data_record):
        return DataRecord(**dict(zip(self.headers, data_record)))


class DummyDataSource(DataSource):
    MR = DataRecord()

    def __init__(self):
        super().__init__()
        self.done = False

    def get_next(self):
        if self.done:
            raise DataSourceFinished()
        else:
            self.done = True
            return DummyDataSource.MR

    def should_exclude(self, data_record):
        return False


class SingleDataRecordSource(DataSource):
    def __init__(self, record):
        super().__init__()
        self.record = record
        self.done = False

    def get_next(self):
        if not self.is_terminated() and not self.done:
            self.done = True
            return self.record
        else:
            raise DataSourceFinished()

    def should_exclude(self, data_record):
        return False


class DataArrayDataSource(DataSource):
    def __init__(self, records):
        super().__init__()
        self.records = records
        self.__iter = iter(self.records)

    def get_next(self):
        return next(self.__iter)

    def should_exclude(self, data_record):
        return False


class DataFunctionDataSource(DataSource):
    def __init__(self, func, *vargs, **kwargs):
        super().__init__()
        self.func = func
        self.vargs = vargs
        self.kwargs = kwargs
        try:
            self.__iter = iter(self.func(*self.vargs, **self.kwargs))
        except:
            raise Exception("data_function should return an object that is an iterable.")

    def get_next(self):
        obj = next(self.__iter)
        if isinstance(obj, DataRecord):
            return obj
        elif type(obj) is tuple or type(obj) is list:
            return DataRecord(*obj)
        elif type(obj) is dict:
            return DataRecord(**obj)
        else:
            return DataRecord(obj)

    def terminate(self):
        super().terminate()
        # self.ds.terminate()

    def should_exclude(self, data_record):
        return False


class DataClassDataSource(DataSource):
    def __init__(self, dclass, *vargs, **kwargs):
        super().__init__()
        self.klass = dclass
        self.vargs = vargs
        self.kwargs = kwargs
        try:
            self.__iter = iter(self.klass(*self.vargs, **self.kwargs))
        except:
            raise Exception("data_class should implement Python iteration protocol.")

    def get_next(self):
        obj = next(self.__iter)
        if isinstance(obj, DataRecord):
            return obj
        elif type(obj) is tuple or type(obj) is list:
            return DataRecord(*obj)
        elif type(obj) is dict:
            return DataRecord(**obj)
        else:
            return DataRecord(obj)

    def terminate(self):
        super().terminate()
        # self.ds.terminate()

    def should_exclude(self, data_record):
        return False


class MultiDataSource(DataSource):
    def __init__(self, dsource_defs):
        super().__init__()
        self.dsdefs = dsource_defs
        self.current_dsource = None
        self.def_iter = iter(self.dsdefs)

    def __init_next_source(self):
        try:
            dsdef = next(self.def_iter)
            self.current_dsource = dsdef.build()
        except:
            raise StopIteration()

    def get_next(self):
        if self.current_dsource is None:
            self.__init_next_source()

        try:
            return self.current_dsource.next()
        except StopIteration as e:
            self.__init_next_source()
            return self.get_next()

    def should_exclude(self, data_record):
        return False
