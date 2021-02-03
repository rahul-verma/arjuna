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

from arjuna.tpi.tracker import track

from .base import GuiSource
from .content import GuiSourceContent

@track("trace")
class _GuiFrameSource(GuiSource):
    '''
        Not supported yet.
    '''

    def __init__(self, frame):
        super().__init__()
        self.__frame = frame
        self.__root_source = None
        self.__html_source = None

    def set_root_source(self, src):
        '''
        Once frame switch takes place, this source can not be got. Hence needs to happen
        explicitly at the time of wrapped element finding.
        '''
        self.__root_source = src

    def _load(self):
        self.__frame.focus()
        self.__html_source = self.__frame._get_html_content_from_remote()

    def get_full_content(self):
        return self.get_root_content() + self.get_inner_content()

    def get_inner_content(self):
        return self.__html_source.get_full_content()

    def get_text_content(self):
        return self.__html_source.get_text_content()

    def get_root_content(self):
        return self.__root_source