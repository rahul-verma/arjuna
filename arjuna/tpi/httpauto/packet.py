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
from arjuna.tpi.engine.asserter import AsserterMixIn


class HttpPacket(AsserterMixIn, metaclass=abc.ABCMeta):

    def __init__(self, http_msg):
        super().__init__()
        self.__http_msg = http_msg

    @property
    def headers(self) -> dict:
        ''' 
            HTTP Headers for this message.
        '''
        return self.__http_msg.headers

    def assert_empty_content(self, *, msg):
        '''
            Validates if content is empty.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if self.headers['Content-Length'] != '0':
            raise AssertionError("Content is not empty.")

    def assert_non_empty_content(self, *, msg):
        '''
            Validates if content is empty.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if self.headers['Content-Length'] == '0':
            raise AssertionError("Content is empty.")

    def assert_header_match(self, header, value=None, *, msg):
        '''
            Validates the presence and optionally the value of an HTTP Header.

            Arguments:
                header: Name of header
                value: Text contained in header. If not provided, then only presence of header is checked.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''
        if header not in self.headers:
            raise AssertionError(f">>{header}<< not present in HTTP Request. {msg}")

        if value is not None:
            actual = self.headers[header]
            if actual != value:
                raise AssertionError(f"Value >>header<< is {actual} but was expected to be {value}. {msg}.")

    def assert_header_mismatch(self, header, value=None, *, msg):
        '''
            Validates the absence of header or mismatch of its content with provided value.

            Arguments:
                header: Name of header
                value: Text contained in header. If not provided, then only absence of header is checked.

            Keyword Arguments:
                msg: A context string explaining why this assertion was done.
        '''

        if value is None:
            if header in self.headers:
                raise AssertionError(f">>{header}<< is present in HTTP Request. {msg}")
        else:
            actual = self.headers[header]
            if actual == value:
                raise AssertionError(f"Value >>header<< is {actual}. It was expected to be different. {msg}.")

