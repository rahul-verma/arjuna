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
import base64

from arjuna.tpi.tracker import track

@track("trace")
class Image:
    '''
        An image object.

        Keyword Arguments:
            fpath: (Mandatory) Absolute path of the Image file.
            b64: Base64 representation of the image.
    '''

    def __init__(self, *, fpath: str, b64: str=None):
        self.__fpath = fpath
        self.__b64 = b64

    @property
    def file_name(self) -> str:
        '''
            File Name of screenshot file.
        '''

        return os.path.basename(self.__fpath)

    @property
    def full_path(self) -> str:
        '''
           Absolute path of screenshot file.
        '''

        return self.__fpath

    @property
    def base64(self) ->str:
        '''
            Base64 string for the image.
        '''
        if self.__b64:
            return self.__b64

        with open(self.__fpath, "rb") as f:
            content = f.read()
            return base64.b64encode(content)

