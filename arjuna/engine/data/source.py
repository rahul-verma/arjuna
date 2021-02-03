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

import abc
import threading
import types

from arjuna.core.reader.excel import *
from arjuna.core.reader.ini import *
from arjuna.tpi.parser.text import *
from arjuna.core.thread import decorators
from arjuna.tpi.error import *
from arjuna.core.error import *
from arjuna.core.types import constants
from arjuna.tpi.data.record import *
from arjuna.engine.data.record import *
# from arjuna.core.utils import sys_utils

class DataSource(metaclass=abc.ABCMeta):
    def __init__(self, *, context):
        super().__init__()
        self.lock = threading.RLock()
        self.name = None
        self.ended = False
        self.__context = context

    @property
    def context(self):
        return self.__context

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
        except StopIteration:
            raise DataSourceFinished("Records Finished.")
        except Exception as e:
            import traceback
            traceback.print_exc()
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

    @abc.abstractmethod
    def reset(self):
        pass

    @property
    def all_records(self):
        out = []
        while True:
            try:
                record = self.next()
                out.append(record)
            except DataSourceFinished as e:
                break
        return out


class FileDataSource(DataSource, metaclass=abc.ABCMeta):
    def __init__(self, path, *, context):
        super().__init__(context=context)
        self.__path = path
        self.__reader = None

    @property
    def path(self):
        return self.__path

    @property
    def reader(self):
        return self.__reader

    @reader.setter
    def reader(self, reader):
        self.__reader = reader

    def get_next(self):
        return self.reader.next()

    def should_exclude(self, data_record):
        return False

    def reset(self):
        self._load_file()

    @abc.abstractmethod
    def _load_file(self):
        pass

class DsvFileMapDataSource(FileDataSource):
    def __init__(self, path, delimiter="\t", *, context):
        super().__init__(path, context=context)
        self.__delimiter = delimiter
        self._load_file()

    def process(self, data_record):
        return DataRecord(context=self.context, **dict(data_record))

    def _load_file(self):
        self.reader = DelimTextFileWithLineAsMap(self.path, delimiter=self.__delimiter)


class IniFileDataSource(FileDataSource):
    def __init__(self, path, *, context):
        super().__init__(path, context=context)
        if path.lower().endswith("ini"):
            self._load_file()
        else:
            raise Exception("Unsupported file extension for Ini reading.")

    def process(self, data_record):
        return DataRecord(context=self.context, **dict(data_record))

    def _load_file(self):
        self.reader = IniFile2MapReader(self.path)


class ExcelFileMapDataSource(FileDataSource):
    def __init__(self, path, *, context):
        super().__init__(path, context=context)
        if path.lower().endswith("xls"):
            self._load_file()
        else:
            raise Exception("Unsupported file extension for Excel reading.")

    def _load_file(self):
        self.reader = ExcelRow2MapReader(self.path)

    def should_exclude(self, data_record):
        return data_record._should_exclude()

    def process(self, data_record):
        return DataRecord(context=self.context, **dict(data_record))

class DummyDataSource(DataSource):

    def __init__(self, *, context):
        super().__init__(context=context)
        self.done = False

    def get_next(self):
        if self.done:
            raise DataSourceFinished()
        else:
            self.done = True
            return DataRecord(context=self.context)

    def should_exclude(self, data_record):
        return False


class SingleDataRecordSource(DataSource):
    def __init__(self, record, *, context):
        super().__init__(context=context)
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

    def reset(self):
        pass


class DataArrayDataSource(DataSource):
    def __init__(self, records, *, context):
        super().__init__(context=context)
        self.records = records
        self.__iter = iter(self.records)

    def get_next(self):
        return next(self.__iter)

    def should_exclude(self, data_record):
        return False

    def reset(self):
        self.__iter = iter(self.records)


class DataFunctionDataSource(DataSource):
    def __init__(self, func, *vargs, context, **kwargs):
        super().__init__(context=context)
        self.func = func
        self.vargs = vargs
        self.kwargs = kwargs
        try:
            self.reset()
        except:
            raise Exception("data_function should return an object that is an iterable.")

    def reset(self):
        self.__iter = iter(self.func(*self.vargs, **self.kwargs))

    def get_next(self):
        obj = next(self.__iter)
        if isinstance(obj, DataRecord):
            return obj
        elif type(obj) is tuple or type(obj) is list:
            return DataRecord(context=self.context, *obj)
        elif type(obj) is dict:
            return DataRecord(context=self.context, **obj)
        else:
            return DataRecord(obj, context=self.context)

    def terminate(self):
        super().terminate()
        # self.ds.terminate()

    def should_exclude(self, data_record):
        return False


class DataClassDataSource(DataSource):
    def __init__(self, dclass, *vargs, context, **kwargs):
        super().__init__(context=context)
        self.klass = dclass
        self.vargs = vargs
        self.kwargs = kwargs
        try:
            self.reset()
        except:
            raise Exception("data_class should implement Python iteration protocol.")

    def reset(self):
        self.__iter = iter(self.klass(*self.vargs, **self.kwargs))

    def get_next(self):
        obj = next(self.__iter)
        if isinstance(obj, DataRecord):
            return obj
        elif type(obj) is tuple or type(obj) is list:
            return DataRecord(context=self.context, *obj)
        elif type(obj) is dict:
            return DataRecord(context=self.context, **obj)
        else:
            return DataRecord(obj, context=self.context)

    def terminate(self):
        super().terminate()
        # self.ds.terminate()

    def should_exclude(self, data_record):
        return False


class MultiDataSource(DataSource):
    def __init__(self, dsource_defs, *, context):
        super().__init__(context=context)
        self.dsdefs = dsource_defs
        self.current_dsource = None
        self.def_iter = iter(self.dsdefs)

    def __init_next_source(self):
        try:
            dsdef = next(self.def_iter)
            self.current_dsource = dsdef.build(context=self.context)
        except:
            raise StopIteration()

    def reset(self):
        self.def_iter = iter(self.dsdefs)

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
