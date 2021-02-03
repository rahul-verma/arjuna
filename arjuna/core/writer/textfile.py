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

import os


class FileWriter:
    def __init__(self, file_path):
        self._fpath = file_path
        self._f = open(self._fpath, "w")

    def close(self):
        self._f.close()

    def write(self, content):
        self._f.write(content)

    def _get_file(self):
        return self._f


class FileLineWriter(FileWriter):
    def write(self, line):
        self._f.write(line + os.linesep)


class FileArray2LineWriter(FileWriter):
    def __init__(self, file_path, delimiter=","):
        super().__init__(file_path)
        self.delimiter = delimiter

    def write(self, line_parts):
        super().write(self.delimiter.join(line_parts))
