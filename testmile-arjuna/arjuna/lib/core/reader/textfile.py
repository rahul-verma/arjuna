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

import os

from arjuna.lib.core.utils import data_utils
from arjuna.lib.core.types import constants

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


class FileLineReader(FileReader):
    def __iter__(self):
        return self

    def next(self):
        l = self._f.readline()
        if not l:
            raise StopIteration()
        elif l.strip().startswith('#'):
            return self.next()
        else:
            return l.rstrip()

    def read(self):
        return self._f.readlines()


class FileLine2ArrayReader(FileLineReader):
    def __init__(self, file_path, delimiter="\t"):
        super().__init__(file_path)
        self.delimiter = delimiter
        self.headers = None
        self._populate_headers()

    def _populate_headers(self):
        try:
            self.headers = self.next()
        except:
            raise Exception("Invalid input file data. Empty headers line.")

    def next(self):
        l = super().next()
        rval = self.process(l)
        return rval

    def process(self, l):
        return data_utils.split(l.rstrip(), self.delimiter)

    def get_headers(self):
        return self.headers

    def read(self):
        return [self.process(l) for l in self]


class FileLine2MapReader(FileLine2ArrayReader):
    def process(self, l):
        l_parts = super().process(l)
        if len(self.headers) != len(l_parts):
            raise Exception(
                "Invalid input file data. Number of headers and data values do not match.{0}Headers:{1}{0}Data values:{2}{0}".format(
                    os.linesep, self.headers, l_parts))
        else:
            return dict(zip(self.headers, l_parts))

    def _populate_headers(self):
        self.headers = super().next()

    def next(self):
        data = self.process(super().next())
        l_keys = {k.lower(): k for k in data}
        if "exclude" in l_keys:
            ex = data[l_keys["exclude"]]
            if ex.upper() in constants.TRUES:
                self.next()
            del ex
        return data
