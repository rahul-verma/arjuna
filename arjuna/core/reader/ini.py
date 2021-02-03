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

import configparser


class IniFile2MapReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self._f = configparser.ConfigParser()
        self._f.read(self.file_path)
        self.sections = self._f.sections()

    def __get_section_data(self, section):
        return self._f[section]

    def __iter__(self):
        return self

    def next(self):
        if self.sections:
            return self.__get_section_data(self.sections.pop(0))
        else:
            raise StopIteration()

    def read(self):
        section_data = {}
        for section in self.sections:
            section_data[section] = dict(self._f[section])
        return section_data

    def close(self):
        self._f.clear()
        del self._f
