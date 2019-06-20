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
from .exceptions import *
from arjuna.setu.types import SetuManagedObject
from arjuna.lib.types import constants
# from arjuna.lib.utils import sys_utils


class ListDataRecord:

    def __init__(self, data_record):
        self.__data_record = data_record

    @property
    def record(self):
        return self.__data_record


class MapDataRecord:

    def __init__(self, data_record):
        self.__data_record = {i.lower():j for i,j in dict(data_record).items()}

    @property
    def record(self):
        return self.__data_record

    def should_exclude(self):
        if "exclude" not in self.__data_record:
            return False

        exclude = self.__data_record['exclude']
        if exclude.upper() in constants.TRUES:
            return True
        else:
            del self.__data_record["exclude"]
            return False


class DataSource(SetuManagedObject, metaclass=abc.ABCMeta):
    def __init__(self):
        super().__init__()
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


class FileDataSource(DataSource, metaclass=abc.ABCMeta):
    def __init__(self, path):
        super().__init__()
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


class DsvFileListDataSource(FileDataSource):
    def __init__(self, path, delimiter="\t"):
        super().__init__(path)
        self.__delimiter = delimiter
        self._load_file()

    def process(self, data_record):
        return ListDataRecord(data_record)

    def _load_file(self):
        self.reader = FileLine2ArrayReader(self.path, self.__delimiter)


class DsvFileMapDataSource(FileDataSource):
    def __init__(self, path, delimiter="\t"):
        super().__init__(path)
        self.__delimiter = delimiter
        self._load_file()

    def process(self, data_record):
        return MapDataRecord(data_record)

    def _load_file(self):
        self.reader = FileLine2MapReader(self.path, self.__delimiter)


class IniFileDataSource(FileDataSource):
    def __init__(self, path):
        super().__init__(path)
        if path.lower().endswith("ini"):
            self._load_file()
        else:
            raise Exception("Unsupported file extension for Ini reading.")

    def process(self, data_record):
        return MapDataRecord(data_record)

    def _load_file(self):
        self.reader = IniFile2MapReader(self.path)


class ExcelFileListDataSource(FileDataSource):
    def __init__(self, path):
        super().__init__(path)
        if path.lower().endswith("xls"):
            self._load_file()
        else:
            raise Exception("Unsupported file extension for Excel reading.")

    def _load_file(self):
        self.reader = ExcelRow2ArrayReader(self.path)

    def should_exclude(self, data_record):
        return False

    def process(self, data_record):
        return ListDataRecord(data_record)


class ExcelFileMapDataSource(FileDataSource):
    def __init__(self, path):
        super().__init__(path)
        if path.lower().endswith("xls"):
            self._load_file()
        else:
            raise Exception("Unsupported file extension for Excel reading.")

    def _load_file(self):
        self.reader = ExcelRow2MapReader(self.path)

    def should_exclude(self, data_record):
        return data_record.should_exclude()

    def process(self, data_record):
        return MapDataRecord(data_record)