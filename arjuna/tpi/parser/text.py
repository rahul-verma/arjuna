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
import re

from arjuna.core.utils import data_utils
from arjuna.core.types import constants


class TextFile:
    '''
    Represents a text file in Read mode.

    Arguments:
        fpath: Absolute path of text file.
    '''

    def __init__(self, fpath):
        self._fpath = fpath
        self._f = open(self._fpath, "r")

    def close(self):
        '''
           Close the file handle.
        '''
        self._f.close()

    def read(self) -> str:
        '''
           Read contents of text file.

           Returns:
                Content of text file as a Python str object.
        '''
        return self._f.read()

    def _get_file(self):
        return self._f


class _TextResource(TextFile):
    def __init__(self, file_name):
        super().__init__(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.sep.join(["../..", "res", file_name]))))


class TextFileAsLines:
    '''
        Represents a text file in Read mode to get line by line content.

        Arguments:
            fpath: Absolute path of text file.

        Keyword Arguments:
            **formatters: Arbitrary key-value arguments to format a line before returning.

        Note:
            You can loop over this object:

                .. code-block:: python

                    for line in fobj:
                        # Do something about the content
                        print(line)
    '''

    def __init__(self, fpath, **formatters):
        self.__filereader = open(fpath, "r")
        self.__formatters = formatters

    def __iter__(self):
        return self

    def next(self) -> str:
        '''
            Get next line.

            Returns:
                Line as a Python str object.
        '''
        l = self.__filereader.readline()
        if not l:
            self.close()
            raise StopIteration()           
        elif l.strip().startswith('#'):
            return self.next()
        else:
            if self.__formatters:
                return l.rstrip().format(**self.__formatters)
            else:
                return l.rstrip()

    __next__ = next

    def close(self):
        '''
           Close the file handle.
        '''
        self.__filereader.close()


class DelimTextFileWithLineAsSeq:
    '''
        Represents a text file in Read mode to get line by line content split by defined delimiter.

        Arguments:
            fpath: Absolute path of text file.

        Keyword Arguments:
            delimiter: (Optional) Delimiter that separates different parts of line. Default is tab (\t)
            header_line_present: (Optional) If True, the first line is treated as a header line.

        Note:
            You can loop over this object:

                .. code-block:: python

                    for line_parts in fobj:
                        # Do something about the parts of a current line
                        print(line_parts)
    '''

    def __init__(self, fpath, *, delimiter="\t", header_line_present=True):
        self.__filereader = TextFileAsLines(fpath)
        self.delimiter = delimiter
        self.__headers = None
        self._populate_headers()

    def __iter__(self):
        return self

    def _populate_headers(self):
        try:
            self.__headers = self.next()
        except:
            raise Exception("Invalid input file data. Empty headers line.")

    def next(self) -> tuple:
        '''
            Get next line parsed based on delimiter as a tuple.

            Returns:
                Line as a Python tuple object.
        '''
        line = self.__filereader.next()
        return data_utils.split(line.rstrip(), self.delimiter)

    __next__ = next

    @property
    def headers(self) -> tuple:
        '''
            Get header line parsed based on delimiter as a tuple.

            Returns:
                Header line as a Python tuple object. None if header line is not present.
        '''
        return self.__headers

    def close(self):
        '''
           Close the file handle.
        '''
        self.__filereader.close()


class DelimTextFileWithLineAsMap:
    '''
        Represents a text file in Read mode to get line by line content split by defined delimiter.

        The first line is treated as a header line.

        Arguments:
            fpath: Absolute path of text file.

        Keyword Arguments:
            delimiter: (Optional) Delimiter that separates different parts of line. Default is tab (\t)

        Note:
            You can loop over this object:

                .. code-block:: python

                    for line_parts in fobj:
                        # Do something about the parts of a current line
                        print(line_parts)
    '''

    def __init__(self, fpath, *, delimiter="\t"):
        self.__filereader = DelimTextFileWithLineAsSeq(fpath, delimiter=delimiter)

    def __iter__(self):
        return self

    @property
    def headers(self) -> tuple:
        '''
            Get header line parsed based on delimiter as a tuple.

            Returns:
                Header line as a Python tuple object.
        '''
        return self.__filereader.headers

    def close(self):
        '''
           Close the file handle.
        '''
        self.__filereader.close()

    def next(self) -> dict:
        '''
            Get next line parsed based on delimiter converted into a Python dictionary based on header line.

            Returns:
                Line as a Python dict object.
        '''
        line_parts = self.__filereader.next()

        if len(self.headers) != len(line_parts):
            raise Exception(
                "Invalid input file data. Number of headers and data values do not match.{0}Headers:{1}{0}Data values:{2}{0}".format(
                    os.linesep, self.headers, line_parts))
        else:
            return dict(zip(self.headers, line_parts))

    __next__ = next

from arjuna.tpi.engine.asserter import AsserterMixIn

class Text(AsserterMixIn):
    '''
    Provides factory methods for dealing with reading text file content in various forms.
    '''
    def __init__(self, text):
        super().__init__()
        self.__content = text

    @property
    def content(self):
        return self.__content

    def assert_contains(self, sub_str, *, msg):
        self.asserter.assert_true(sub_str in self.content, msg="Sub string {} not found in {}. ".format(sub_str, self.content) + msg)

    def findall(self, repattern):
        return re.findall(repattern, self.content)

    def find(self, repattern):
        all = re.findall(repattern, self.content)
        if all:
            return all[0]
        else:
            raise Exception(f"No match found for {repattern} in {self.content}")

    def exists(self, repattern):
        matches = re.findall(repattern, self.content)
        if matches:
            return True
        else:
            return False

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content

    def __eq__(self, other):
        return self.content == other

    @classmethod
    def file_content(cls, fpath) -> str:
        '''
            Get content of a text file.

            Arguments:
                fpath: Absolute path of text file.

            Returns:
                Content of text file as Python str object.
        '''
        f = TextFile(fpath)
        content = f.read()
        f.close()
        return content

    @classmethod
    def file_lines(cls, fpath) -> TextFileAsLines:
        '''
            Get a reader for text file in Read mode to get line by line content.

            Arguments:
                fpath: Absolute path of text file.

            Returns:
                Arjuna's TextFileAsLines object.

            Note:
                You must explicitly close the returned object by calling its **close()** method.
        '''
        return TextFileAsLines(fpath)

    @classmethod
    def delimited_file(cls, fpath, *, delimiter="\t", header_line_present=True) -> 'DelimTextFileWithLineAsMap OR DelimTextFileWithLineAsSeq':
        '''
            Represents a text file in Read mode to get line by line content split by defined delimiter.

            Arguments:
                fpath: Absolute path of text file.

            Keyword Arguments:
                delimiter: (Optional) Delimiter that separates different parts of line. Default is tab (\t)
                header_line_present: (Optional) If True, the DelimTextFileWithLineAsMap is created, else DelimTextFileWithLineAsSeq is created to represent the file.

            Note:
                You can loop over the returned object:

                    .. code-block:: python

                        for line in fobj:
                            # Do something about the parts of a current line
                            print(line)

                The line is a tuple of parts for DelimTextFileWithLineAsSeq object and is a dictionary for DelimTextFileWithLineAsMap object.

            Note:
                You must explicitly close the returned object by calling its **close()** method.
        '''
        if header_line_present:
            return DelimTextFileWithLineAsMap(fpath, delimiter=delimiter)
        else:
            return DelimTextFileWithLineAsSeq(fpath, delimiter=delimiter)
