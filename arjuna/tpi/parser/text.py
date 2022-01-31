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
from arjuna.tpi.data.entity import _DataEntity

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

class Text(str, AsserterMixIn):
    '''
        Arjuna representation of a String.
        Provides factory methods for dealing with reading text file content in various forms.

        Arguments:
            text: Input string. If a non-string object is provided it str(text) is called.
            fargs: Arbitrary positional arguments for formatting the string.

        Keyword Arguments:
            fnargs: Arbitrary named arguments (keworg arguments) for formatting the string.
    '''
    def __init__(self, text, *fargs, **fnargs):
        str.__init__(text)
        AsserterMixIn.__init__(self)
        self.__content = text
        self.__do_eval = False
        if type(self.__content) is not str:
            self.__do_eval = True
            self.__content = str(self.__content)
        self.__fargs = fargs
        self.__fnargs = fnargs
        if self.__fargs or self.__fnargs:
            self.format(*self.__fargs, **self.__fnargs)

    def format(self, *fargs, **fnargs):
        '''
            Format the string using provided named and keyword arguments.

            Positional arguments are used to format $$ placeholders as per the order in which they are found.

            Keyword/named arguments are used to format $<name>$ placeholders. Order does not matter.

            Supports C/L/R queries as names of placeholders.

            The provided features are very advanced. Refer Arjuna documentation for use cases and examples.

            Arguments:
                fargs: Arbitrary positional arguments for formatting the string.

            Keyword Arguments:
                fnargs: Arbitrary named arguments (keworg arguments) for formatting the string.
        '''

        target = self.__content

        def get_global_value(in_str):
            from arjuna import C, L, R
            gtype, query = in_str.split(".", 1)
            gtype = gtype.upper()
            return locals()[gtype](query)

        pos_pattern = r"(\$\s*\$)"
        named_pattern = r"\$(\s*[\w\.]+?\s*)\$"
        fmt_target = target.replace("{", "__LB__").replace("}", "__RB__")

        # Find params
        pos_matches = re.findall(pos_pattern, fmt_target)
        named_matches = re.findall(named_pattern, fmt_target)

        if pos_matches and named_matches:
            for match in named_matches:
                match = match.lower().strip()
                if not match.startswith("c.") and not match.startswith("l.") and not match.startswith("r."):
                    raise Exception("You can not use positional $$ placeholders and named $<name>$ placholders together in a withx locator definition (except those with C./L./R. prefixes to fetch global values. Wrong withx definition: " + target)

        if pos_matches:
            if not fargs:
                fargs = tuple()    
            if len(pos_matches) != len(fargs):
                raise Exception("Number of positional arguments supplied to format withx locator do not match number of $$ placeholders. Placeholders: {}. Positional args: {}. Wrong usage of withx locator: {}".format(len(pos_matches), fargs, target))

            for i,match in enumerate(pos_matches):
                fmt_target = fmt_target.replace(match, "{}")

            fmt_target = fmt_target.format(*fargs)

        def get_value_from_container(name, *, container=None):
            if container is None:
                parts = name.split(".", 1)
                if len(parts) == 1:
                    # It is reference directly to an object and if present could have been resolved before this logic hits.
                    return "__NOTFOUND"
                container, name = parts

            name_parts = re.split(r'([\.\[])', name, 1) # Will return single element list or 3 part list: name, delim, rest
            if len(name_parts) == 1:
                name, delim, rest = name, "", ""
            else:
                name, delim, rest = name_parts

            try:
                container = fnargs[container]
                if type(container) is dict:
                    first_obj = container[name]
                elif isinstance(type(container), _DataEntity):
                    first_obj = getattr(container, name)
                if delim == "":
                    return first_obj
                else:
                    return eval(f"first_obj{delim}{rest}")
            except Exception as e:
                return "__NOTFOUND"                 
            
        for match in named_matches:
            names_set = None
            target = "${}$".format(match)
            processed_name = match.lower().strip()
            repl_value = None
            if processed_name.startswith("c.") or processed_name.startswith("l.") or processed_name.startswith("r."):
                repl_value = get_global_value(processed_name)
            elif processed_name.startswith("data."):
                processed_name = processed_name.split(".")[1]
                if 'data' in fnargs:
                    temp_val = get_value_from_container(processed_name, container="data")
                    if temp_val == "__NOTFOUND":
                        continue
                    else:
                        repl_value = temp_val
                else:
                    continue
            else:
                if processed_name not in fnargs:
                    # Try a container and dynamic logic like a.b.c or a.b[3]
                    temp_val = get_value_from_container(processed_name)
                    if temp_val != "__NOTFOUND":
                        repl_value = temp_val
                    else:
                        if 'data' in fnargs:
                            temp_val = get_value_from_container(processed_name, container="data")
                            if temp_val == "__NOTFOUND":
                                continue
                            else:
                                repl_value = temp_val
                        else:
                            continue
                else:
                    repl_value = fnargs[processed_name]

            fmt_target = fmt_target.replace(target, str(repl_value))

        fmt_target = fmt_target.replace("__LB__", "{").replace("__RB__", "}")
        if self._eval:
            fmt_target = eval(fmt_target)

        self.__content = fmt_target
        return self.__content

    @property
    def content(self):
        return self.__content

    @property
    def _eval(self):
        return self.__do_eval

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

    def find_links(self, *, unique=True, contain=""):
        def remove_trailing_slash(full_link):
            if full_link.endswith("/"):
                return full_link[:-1]
            else:
                return full_link

        def remove_quotes(s):
            return s.replace('"', "").replace("'", "")

        r = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        out = []
        for k in self.findall(r):
            if type(k) is str:
                if k:
                    out.append(remove_quotes(k))
            else:
                out.extend([remove_quotes(i) for i in k if i.strip()])
        
        out = [remove_trailing_slash(i) for i in out]

        # Filter
        out = [o for o in out if contain in o]

        if unique:
            return tuple(set(out))
        else:
            return tuple(out)

    @property
    def links(self):
        self.get_links()

    @property
    def unique_links(self):
        self.get_links(unique=True)
        

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
        if isinstance(other, Text):
            return self.content == other.content
        else:
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
