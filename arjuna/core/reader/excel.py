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

import xlrd


class ExcelRowReader:
    def __init__(self, path):
        self.wb = xlrd.open_workbook(path)
        self.sheet = self.wb.sheet_by_name(self.wb.sheet_names()[0])
        self.rcount = self.sheet.nrows
        self.ccount = self.sheet.ncols
        self.curent_row_index = -1
        self.validate()

    def __iter__(self):
        return self

    def read_next_row(self):
        self.curent_row_index += 1
        if self.curent_row_index < self.rcount:
            return self.sheet.row(self.curent_row_index)
        else:
            raise Exception("Done")

    def next(self):
        try:
            return self.process(self.read_next_row())
        except:
            self.close()
            raise StopIteration()

    __next__ = next

    def read(self):
        return [r for r in iter(self)]

    def process(self, row):
        return row

    def validate(self):
        pass

    def close(self):
        pass
        #self.wb.close()


class ExcelRow2ArrayReader(ExcelRowReader):
    def __init__(self, path):
        super().__init__(path)
        self.__headers = []
        self._populate_headers()

    def get_headers(self):
        return self.__headers

    @property
    def headers(self):
        return self.__headers

    def _populate_headers(self):
        self.__headers = [h.value for h in self.read_next_row()]

    def process(self, row):
        return [h.value for h in row]

    def validate(self):
        if self.rcount == 0:
            raise Exception("Empty or wrongly formattted Excel file. Is first line empty?")

    def __iter__(self):
        return self

    def next(self):
        return super().next()

class ExcelRow2MapReader(ExcelRow2ArrayReader):
    def __init__(self, path):
        super().__init__(path)

    def process(self, row):
        return dict(zip(self.headers, super().process(row)))
