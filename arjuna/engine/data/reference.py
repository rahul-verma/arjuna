'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

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

from arjuna.core.reader.excel import *
from .record import *


class ContextualDataReference(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def record_for(self, context):
        pass

class __ExcelDataReference(ContextualDataReference):
    def __init__(self, path, key_column=None):
        self.map = {}
        self.path = path
        self.key_column = key_column
        if (path.lower().endswith("xls")):
            self.reader = ExcelRow2ArrayReader(path)
        else:
            raise Exception("Unsupported file format for Excel reading.")

        self._populate()

    @abc.abstractmethod
    def _populate(self):
        pass

    def record_for(self, context):
        if context.lower() in self.map:
            return self.map[context.lower()]
        else:
            raise Exception("{} at {} does not contain {} context key.".format(self.__class__.__name__, self.path, context))

class ExcelRowDataReference(__ExcelDataReference):

    def __init__(self, path):
        super().__init__(path)

    def _populate(self):
        names = self.reader.headers[1:]
        while True:
            try:
                data_record = self.reader.next()
            except StopIteration:
                break
            else:
                self.map[data_record[0].lower()] = DataRecord(**dict(zip(names, data_record[1:])))
        self.reader.close()


class ExcelColumnDataReference(__ExcelDataReference):

    def __init__(self, path):
        super().__init__(path)

    def _populate(self):
        contexts = self.reader.headers[1:]
        cmap = {i: {} for i in contexts}
        while True:
            try:
                data_record = self.reader.next()
            except StopIteration:
                break
            else:
                name = data_record[0]
                for index, context in enumerate(contexts):
                    cmap[context][name] = data_record[index+1]
        self.reader.close()
        for context, kv in cmap.items():
            self.map[context.lower()] = DataRecord(**kv)
