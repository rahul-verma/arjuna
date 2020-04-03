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

import os

from arjuna.core.utils import data_utils
from arjuna.core.types import constants


class FileReader:
    def __init__(self, file_path):
        self._fpath = file_path
        self._f = open(self._fpath, "r")

    def close(self):
        self._f.close()

    def read(self):
        return self._f.read()

    def _get_file(self):
        return self._f


class TextResourceReader(FileReader):
    def __init__(self, file_name):
        super().__init__(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.sep.join(["../..", "res", file_name]))))


class FileLineReader:
    def __init__(self, file_path):
        self.__filereader = open(file_path, "r")

    def __iter__(self):
        return self

    def next(self):
        l = self.__filereader.readline()
        if not l:
            self.close()
            raise StopIteration()
        elif l.strip().startswith('#'):
            return self.next()
        else:
            return l.rstrip()

    def close(self):
        self.__filereader.close()


class FileLine2ArrayReader:
    def __init__(self, file_path, delimiter="\t"):
        self.__filereader = FileLineReader(file_path)
        self.delimiter = delimiter
        self.headers = None
        self._populate_headers()

    def _populate_headers(self):
        try:
            self.headers = self.next()
        except:
            raise Exception("Invalid input file data. Empty headers line.")

    def next(self):
        line = self.__filereader.next()
        return data_utils.split(line.rstrip(), self.delimiter)

    def get_headers(self):
        return self.headers

    def close(self):
        self.__filereader.close()


class FileLine2MapReader:
    def __init__(self, file_path, delimiter="\t"):
        self.__filereader = FileLine2ArrayReader(file_path, delimiter)

    def get_headers(self):
        return self.__filereader.headers

    def close(self):
        self.__filereader.close()

    def next(self):
        line_parts = self.__filereader.next()

        if len(self.get_headers()) != len(line_parts):
            raise Exception(
                "Invalid input file data. Number of headers and data values do not match.{0}Headers:{1}{0}Data values:{2}{0}".format(
                    os.linesep, self.get_headers(), line_parts))
        else:
            return dict(zip(self.get_headers(), line_parts))
